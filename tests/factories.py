"""Synthetic SRS-shaped records shared by automated tests; no real student data."""

from datetime import date


def student_fields(**overrides):
    return {
        'student_id': 'PES1UG24CS145',
        'name': 'Sample Student',
        'dob': date(2006, 1, 2),
        'gender': 'Male',
        'course': 'B.Tech CSE',
        'year': 2,
        'mobile': '9000000000',
        'email': 'sample@example.test',
        'guardian_name': 'Sample Guardian',
        'guardian_mobile': '9000000001',
        'address': '',
        **overrides,
    }
