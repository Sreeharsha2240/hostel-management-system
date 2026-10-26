"""Synthetic fixtures shared by the Sprint 2 integration tests."""

from datetime import date

from hostels.models import Hostel, Room
from students.models import Student


def make_student(number=1, **overrides):
    data = {
        "student_id": f"PES1UG24CS{number:03d}",
        "name": f"Sample Student {number}",
        "date_of_birth": date(2005, 1, 2),
        "gender": Student.Gender.MALE,
        "course": "CSE",
        "year": 2,
        "mobile": "9000000000",
        "email": f"sample{number}@example.test",
        "guardian_name": "Sample Guardian",
        "guardian_mobile": "9000000001",
    }
    return Student.objects.create(**(data | overrides))


def make_room(number="101", hostel=None, **overrides):
    hostel = hostel or Hostel.objects.create(name=f"Boys {number}", hostel_type="Boys")
    data = {
        "hostel": hostel,
        "room_number": number,
        "floor": 0,
        "room_type": "Double",
        "capacity": 2,
    }
    return Room.objects.create(**(data | overrides))
