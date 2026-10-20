from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models, transaction
from django.utils import timezone


def validate_birth_date(value):
    if value > timezone.localdate():
        raise ValidationError('Date of birth cannot be in the future.')


mobile_validator = RegexValidator(r'^[0-9]{10}$', 'Enter exactly 10 digits.')


class StudentQuerySet(models.QuerySet):
    def delete(self):
        raise ValidationError('Student records must be deactivated, not deleted.')

    def update(self, **kwargs):
        if {'student_id', 'status'} & kwargs.keys():
            raise ValidationError('Save students individually to enforce ID and allocation rules.')
        return super().update(**kwargs)

    def bulk_create(
        self, objs, batch_size=None, ignore_conflicts=False, update_conflicts=False,
        update_fields=None, unique_fields=None,
    ):
        if update_conflicts and {'student_id', 'status'} & set(update_fields or []):
            raise ValidationError('Student IDs and status cannot be changed by bulk upsert.')
        return super().bulk_create(
            objs, batch_size=batch_size, ignore_conflicts=ignore_conflicts,
            update_conflicts=update_conflicts, update_fields=update_fields,
            unique_fields=unique_fields,
        )


class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'

    class Status(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        INACTIVE = 'Inactive', 'Inactive'

    student_id = models.CharField(
        max_length=13, unique=True,
        validators=[RegexValidator(r'^[A-Za-z0-9]{13}$', 'Enter a 13-character alphanumeric Student ID.')],
        error_messages={'unique': 'Student ID already registered'},
    )
    name = models.CharField(max_length=60, db_index=True)
    dob = models.DateField(validators=[validate_birth_date])
    gender = models.CharField(max_length=6, choices=Gender.choices)
    course = models.CharField(max_length=30)
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    mobile = models.CharField(max_length=10, validators=[mobile_validator])
    email = models.EmailField(max_length=80)
    guardian_name = models.CharField(max_length=60)
    guardian_mobile = models.CharField(max_length=10, validators=[mobile_validator])
    address = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        null=True, blank=True, related_name='student_profile',
    )
    objects = StudentQuerySet.as_manager()

    class Meta:
        ordering = ['name', 'student_id']
        constraints = [
            models.CheckConstraint(condition=models.Q(year__range=(1, 5)), name='student_year_1_5'),
            models.CheckConstraint(condition=models.Q(gender__in=['Male', 'Female']), name='student_valid_gender'),
            models.CheckConstraint(condition=models.Q(status__in=['Active', 'Inactive']), name='student_valid_status'),
        ]

    def clean(self):
        self.student_id = (self.student_id or '').strip().upper()
        for field in ('name', 'course', 'guardian_name'):
            value = (getattr(self, field) or '').strip()
            setattr(self, field, value)
            if not value:
                raise ValidationError({field: 'This field is required.'})
        if self.user_id and self.user.role != 'student':
            raise ValidationError({'user': 'Only a Student account can be linked to a student record.'})

    def save(self, *args, **kwargs):
        from .allocation_access import active_allocation

        with transaction.atomic():
            self.full_clean()
            if self.pk:
                previous = Student.objects.select_for_update().get(pk=self.pk)
                if previous.student_id != self.student_id:
                    raise ValidationError({'student_id': 'Student ID cannot be changed.'}, code='IMMUTABLE_FIELD')
                if previous.status == self.Status.ACTIVE and self.status == self.Status.INACTIVE:
                    allocation = active_allocation(self)
                    if allocation:
                        raise ValidationError(
                            f'Cannot deactivate: student has an active allocation to {allocation.bed}.',
                            code='HAS_ACTIVE_ALLOCATION',
                        )
            return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError('Student records must be deactivated, not deleted.')

    def __str__(self):
        return f'{self.student_id} - {self.name}'
