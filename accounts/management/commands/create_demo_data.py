"""Populate local presentation records without deleting existing data."""

from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from accounts.models import User
from allocations.models import Allocation
from allocations.services import allocate
from hostels.models import Bed, Hostel, Room
from payments.models import Payment
from payments.services import record_payment
from students.models import Student


class Command(BaseCommand):
    help = "Create repeatable local hostel, student, allocation, and payment demo data."

    student_rows = (
        ("DEMO202600001", "Aarav Demo", Student.Gender.MALE, "Computer Science", 2),
        ("DEMO202600002", "Kabir Demo", Student.Gender.MALE, "Information Systems", 3),
        ("DEMO202600003", "Rohan Demo", Student.Gender.MALE, "Computer Science", 1),
        ("DEMO202600004", "Diya Demo", Student.Gender.FEMALE, "Information Systems", 2),
        ("DEMO202600005", "Meera Demo", Student.Gender.FEMALE, "Computer Science", 3),
        ("DEMO202600006", "Anaya Demo", Student.Gender.FEMALE, "Business Studies", 1),
    )

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Demo data may only be created when DJANGO_DEBUG=True.")

        admin = User.objects.filter(username="hms_demo_admin").first()
        student_login = User.objects.filter(username="hms_demo_student").first()
        if not admin or not student_login:
            raise CommandError(
                "Run 'python manage.py create_demo_accounts' first so the demo "
                "Admin and Student logins exist."
            )

        boys_hostel, _ = Hostel.objects.get_or_create(
            name="Demo Boys Hostel",
            defaults={"hostel_type": Hostel.HostelType.BOYS, "is_active": True},
        )
        girls_hostel, _ = Hostel.objects.get_or_create(
            name="Demo Girls Hostel",
            defaults={"hostel_type": Hostel.HostelType.GIRLS, "is_active": True},
        )

        for hostel, room_specs in (
            (
                boys_hostel,
                (
                    ("101", 1, Room.RoomType.TRIPLE, 3),
                    ("102", 1, Room.RoomType.DOUBLE, 2),
                ),
            ),
            (
                girls_hostel,
                (
                    ("201", 2, Room.RoomType.TRIPLE, 3),
                    ("202", 2, Room.RoomType.DOUBLE, 2),
                ),
            ),
        ):
            for room_number, floor, room_type, capacity in room_specs:
                room, _ = Room.objects.get_or_create(
                    hostel=hostel,
                    room_number=room_number,
                    defaults={
                        "floor": floor,
                        "room_type": room_type,
                        "capacity": capacity,
                        "fee_amount": Decimal("12000.00"),
                    },
                )
                # Room.save() synchronizes the reserved demo room's bed records.
                room.save()

        today = timezone.localdate()
        students = {}
        for index, (student_id, name, gender, course, year) in enumerate(
            self.student_rows, start=1
        ):
            student, _ = Student.objects.get_or_create(
                student_id=student_id,
                defaults={
                    "name": name,
                    "date_of_birth": today.replace(year=today.year - 20),
                    "gender": gender,
                    "course": course,
                    "year": year,
                    "mobile": f"90000000{index:02d}",
                    "email": f"{student_id.lower()}@example.test",
                    "guardian_name": f"{name.split()[0]} Guardian",
                    "guardian_mobile": f"90000001{index:02d}",
                    "address": "Demo address",
                    "status": Student.Status.ACTIVE,
                },
            )
            students[student_id] = student

        demo_student = students[self.student_rows[0][0]]
        linked_profile = Student.objects.filter(user=student_login).first()
        if linked_profile is None and demo_student.user_id is None:
            demo_student.user = student_login
            demo_student.save(update_fields=["user"])

        allocation_specs = (
            (self.student_rows[0][0], boys_hostel, "101"),
            (self.student_rows[1][0], boys_hostel, "101"),
            (self.student_rows[3][0], girls_hostel, "201"),
            (self.student_rows[4][0], girls_hostel, "201"),
        )
        for student_id, hostel, room_number in allocation_specs:
            student = students[student_id]
            if Allocation.objects.filter(
                student=student, status=Allocation.AllocationStatus.ACTIVE
            ).exists():
                continue
            bed = (
                Bed.objects.filter(
                    room__hostel=hostel,
                    room__room_number=room_number,
                    status=Bed.BedStatus.AVAILABLE,
                )
                .order_by("label")
                .first()
            )
            if bed is None:
                self.stderr.write(
                    self.style.WARNING(
                        f"No available demo bed for {student.name}; allocation skipped."
                    )
                )
                continue
            allocate(student=student, bed=bed, actor=admin)

        payment_specs = (
            (
                self.student_rows[0][0],
                Decimal("12000.00"),
                "HMSDEMO0001",
                Payment.Mode.UPI,
            ),
            (
                self.student_rows[1][0],
                Decimal("5000.00"),
                "HMSDEMO0002",
                Payment.Mode.CASH,
            ),
            (
                self.student_rows[4][0],
                Decimal("12000.00"),
                "HMSDEMO0003",
                Payment.Mode.BANK_TRANSFER,
            ),
        )
        for student_id, amount, reference, mode in payment_specs:
            if Payment.objects.filter(reference=reference).exists():
                continue
            record_payment(
                actor=admin,
                student=students[student_id],
                amount=amount,
                date=today,
                mode=mode,
                reference=reference,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data is ready: 2 hostels, 4 rooms, 6 student profiles, "
                "up to 4 bed allocations, and 3 sample payments. "
                "Rerunning this command will not delete records or duplicate payments."
            )
        )
