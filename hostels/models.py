from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models, transaction
from django.db.models.deletion import ProtectedError


class Hostel(models.Model):
    class Type(models.TextChoices):
        BOYS = 'Boys', 'Boys'
        GIRLS = 'Girls', 'Girls'

    name = models.CharField(max_length=40, unique=True)
    type = models.CharField(max_length=5, choices=Type.choices)

    class Meta:
        ordering = ['name', 'pk']
        constraints = [models.CheckConstraint(
            condition=models.Q(type__in=['Boys', 'Girls']), name='hostel_valid_type',
        )]

    def clean(self):
        self.name = self.name.strip()
        if not self.name:
            raise ValidationError({'name': 'Enter a hostel name.'})
        if self.pk and Hostel.objects.filter(pk=self.pk).exclude(type=self.type).exists():
            if self.rooms.filter(beds__status='Occupied').exists():
                raise ValidationError({'type': 'Release occupied beds before changing hostel type.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RoomQuerySet(models.QuerySet):
    def update(self, **kwargs):
        if {'capacity', 'room_number', 'hostel', 'hostel_id'} & kwargs.keys():
            raise ValidationError('Save rooms individually to keep their beds consistent.')
        return super().update(**kwargs)

    def bulk_create(self, *args, **kwargs):
        raise ValidationError('Save rooms individually to generate their beds.')

    def bulk_update(self, objs, fields, batch_size=None):
        if {'capacity', 'room_number', 'hostel', 'hostel_id'} & set(fields):
            raise ValidationError(
                'Save rooms individually to keep their beds consistent.',
            )
        return super().bulk_update(objs, fields, batch_size=batch_size)


class Room(models.Model):
    class Type(models.TextChoices):
        SINGLE = 'Single', 'Single'
        DOUBLE = 'Double', 'Double'
        TRIPLE = 'Triple', 'Triple'

    hostel = models.ForeignKey(Hostel, on_delete=models.PROTECT, related_name='rooms')
    room_number = models.CharField(max_length=6, validators=[RegexValidator(
        r'^[A-Za-z0-9]+$', 'Use letters and digits for the room number.',
    )])
    floor = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)])
    room_type = models.CharField(max_length=10, choices=Type.choices)
    capacity = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(4),
    ])
    fee_amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
    )
    objects = RoomQuerySet.as_manager()

    class Meta:
        ordering = ['hostel__name', 'floor', 'room_number', 'pk']
        constraints = [
            models.UniqueConstraint(fields=['hostel', 'room_number'], name='unique_hostel_room'),
            models.CheckConstraint(condition=models.Q(capacity__range=(1, 4)), name='room_capacity_1_4'),
            models.CheckConstraint(condition=models.Q(floor__lte=99), name='room_floor_0_99'),
            models.CheckConstraint(condition=models.Q(fee_amount__gte=0), name='room_fee_nonnegative'),
            models.CheckConstraint(
                condition=models.Q(room_type__in=['Single', 'Double', 'Triple']),
                name='room_valid_type',
            ),
        ]

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                Room.objects.select_for_update().get(pk=self.pk)
            self.full_clean()
            super().save(*args, **kwargs)
            # Reload persisted values so partial saves cannot generate beds
            # using a capacity or room number that was not actually saved.
            current = Room.objects.get(pk=self.pk)
            beds = list(current.beds.select_for_update().order_by('position'))
            excess = [bed for bed in beds if bed.position > current.capacity]
            if any(bed.status != Bed.Status.AVAILABLE for bed in excess):
                raise ValidationError({'capacity': 'Only available excess beds can be removed.'})
            try:
                for bed in excess:
                    bed.delete()
            except ProtectedError:
                raise ValidationError({
                    'capacity': 'Beds with allocation history cannot be removed.',
                }) from None
            retained = {bed.position: bed for bed in beds if bed.position <= current.capacity}
            for position in range(1, current.capacity + 1):
                number = f'{current.room_number}-{chr(64 + position)}'
                if position not in retained:
                    Bed.objects.create(room=current, position=position, bed_number=number)
                elif retained[position].bed_number != number:
                    Bed.objects.filter(pk=retained[position].pk).update(bed_number=number)

    def __str__(self):
        return f'{self.hostel.name} / {self.room_number}'


class Bed(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'Available', 'Available'
        OCCUPIED = 'Occupied', 'Occupied'
        MAINTENANCE = 'Maintenance', 'Under maintenance'

    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='beds')
    position = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(4),
    ])
    bed_number = models.CharField(max_length=8)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.AVAILABLE, db_index=True)

    class Meta:
        ordering = ['room__hostel__name', 'room__room_number', 'position', 'pk']
        constraints = [
            models.UniqueConstraint(fields=['room', 'position'], name='unique_room_bed_position'),
            models.UniqueConstraint(fields=['room', 'bed_number'], name='unique_room_bed_number'),
            models.CheckConstraint(condition=models.Q(position__range=(1, 4)), name='bed_position_1_4'),
            models.CheckConstraint(
                condition=models.Q(status__in=['Available', 'Occupied', 'Maintenance']),
                name='bed_valid_status',
            ),
        ]

    def clean(self):
        if self.room_id and self.position is not None and self.position > self.room.capacity:
            raise ValidationError({'position': 'Bed position exceeds room capacity.'})
        if self.pk and Bed.objects.filter(pk=self.pk).exclude(
            room_id=self.room_id, position=self.position,
        ).exists():
            raise ValidationError('Beds cannot be moved; change room capacity instead.')

    def save(self, *args, **kwargs):
        if self.room_id and self.position is not None:
            self.bed_number = f'{self.room.room_number}-{chr(64 + self.position)}'
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.room.hostel.name} / {self.bed_number}'
