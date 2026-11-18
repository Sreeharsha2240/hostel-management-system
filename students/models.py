from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models, transaction


class StudentQuerySet(models.QuerySet):
    def bulk_create(
        self,
        objs,
        batch_size=None,
        ignore_conflicts=False,
        update_conflicts=False,
        update_fields=None,
        unique_fields=None,
    ):
        if update_conflicts:
            raise ValidationError(
                "Save existing students individually to check identity and "
                "active allocations."
            )
        return super().bulk_create(
            objs,
            batch_size=batch_size,
            ignore_conflicts=ignore_conflicts,
            update_conflicts=update_conflicts,
            update_fields=update_fields,
            unique_fields=unique_fields,
        )

    def update(self, **kwargs):
        if "status" in kwargs:
            raise ValidationError(
                "Save student status individually to check active allocations."
            )
        if "student_id" in kwargs:
            raise ValidationError(
                "Student ID cannot be changed.", code="IMMUTABLE_FIELD"
            )
        if "gender" in kwargs:
            raise ValidationError(
                "Save student gender individually to check active allocations."
            )
        return super().update(**kwargs)


class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"

    class Status(models.TextChoices):
        ACTIVE = "Active", "Active"
        INACTIVE = "Inactive", "Inactive"

    student_id = models.CharField(
        max_length=13,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z0-9]{13}$",
                message="Student ID must contain exactly 13 letters or numbers.",
            )
        ],
    )
    name = models.CharField(max_length=60)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, choices=Gender.choices)
    course = models.CharField(max_length=30)
    year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    mobile = models.CharField(
        max_length=10,
        validators=[RegexValidator(r"^\d{10}$", "Enter a 10-digit mobile number.")],
    )
    email = models.EmailField(max_length=80)
    guardian_name = models.CharField(max_length=60)
    guardian_mobile = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(r"^\d{10}$", "Enter a 10-digit guardian mobile number.")
        ],
    )
    address = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="student_profile",
        help_text="Optional Student login account allowed to view this profile.",
    )
    status = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = StudentQuerySet.as_manager()

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.student_id} - {self.name}"

    def validate_allocation_gender(self, gender):
        from allocations.models import Allocation
        from hostels.models import Hostel

        hostel_type = {
            self.Gender.MALE: Hostel.HostelType.BOYS,
            self.Gender.FEMALE: Hostel.HostelType.GIRLS,
        }.get(gender)
        if (
            hostel_type
            and Allocation.objects.filter(
                student_id=self.pk, status=Allocation.AllocationStatus.ACTIVE
            )
            .exclude(bed__room__hostel__hostel_type=hostel_type)
            .exists()
        ):
            raise ValidationError(
                "Release this student's active allocation before changing gender.",
                code="GENDER_MISMATCH",
            )

    @transaction.atomic
    def save(self, *args, **kwargs):
        if kwargs.get("update_fields") is not None:
            kwargs["update_fields"] = frozenset(kwargs["update_fields"])
        if self.pk:
            previous = Student.objects.select_for_update().get(pk=self.pk)
            fields = kwargs.get("update_fields")
            if (fields is None or "student_id" in fields) and (
                self.student_id != previous.student_id
            ):
                raise ValidationError(
                    "Student ID cannot be changed.", code="IMMUTABLE_FIELD"
                )
            if (
                fields is None or "gender" in fields
            ) and self.gender != previous.gender:
                self.validate_allocation_gender(self.gender)
            if (
                fields is None or "status" in fields
            ) and self.status == self.Status.INACTIVE:
                from allocations.models import Allocation

                if Allocation.objects.filter(
                    student_id=self.pk, status=Allocation.AllocationStatus.ACTIVE
                ).exists():
                    raise ValidationError(
                        "Release this student's active allocation before deactivation.",
                        code="HAS_ACTIVE_ALLOCATION",
                    )
        return super().save(*args, **kwargs)
