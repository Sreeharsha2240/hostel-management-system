
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Hostel(models.Model):
    class HostelType(models.TextChoices):
        BOYS = "Boys", "Boys"
        GIRLS = "Girls", "Girls"

    name = models.CharField(max_length=100, unique=True)
    hostel_type = models.CharField(max_length=5, choices=HostelType.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Room(models.Model):
    class RoomType(models.TextChoices):
        SINGLE = "Single", "Single"
        DOUBLE = "Double", "Double"
        TRIPLE = "Triple", "Triple"

    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.PROTECT,
        related_name="rooms",
    )
    room_number = models.CharField(max_length=10)
    floor = models.PositiveSmallIntegerField()
    room_type = models.CharField(max_length=10, choices=RoomType.choices)
    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )

    class Meta:
        ordering = ["hostel", "floor", "room_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["hostel", "room_number"],
                name="unique_room_number_per_hostel",
            )
        ]

    def clean(self):
        super().clean()

        if self.capacity and not 1 <= self.capacity <= 4:
            raise ValidationError({"capacity": "Capacity must be between 1 and 4."})

        if self.pk and self.capacity:
            existing_beds = self.beds.count()
            if self.capacity < existing_beds:
                raise ValidationError({
                    "capacity": (
                        f"This room already has {existing_beds} beds. "
                        "Capacity cannot be reduced below the existing bed count."
                    )
                })

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Create any missing beds automatically. Existing beds are preserved.
        labels = ["A", "B", "C", "D"]
        for label in labels[:self.capacity]:
            Bed.objects.get_or_create(
                room=self,
                label=f"{self.room_number}-{label}",
                defaults={"status": Bed.BedStatus.AVAILABLE},
            )

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"


class Bed(models.Model):
    class BedStatus(models.TextChoices):
        AVAILABLE = "Available", "Available"
        OCCUPIED = "Occupied", "Occupied"
        MAINTENANCE = "Maintenance", "Under maintenance"

    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="beds",
    )
    label = models.CharField(max_length=20)
    status = models.CharField(
        max_length=12,
        choices=BedStatus.choices,
        default=BedStatus.AVAILABLE,
    )

    class Meta:
        ordering = ["room", "label"]
        constraints = [
            models.UniqueConstraint(
                fields=["room", "label"],
                name="unique_bed_label_per_room",
            )
        ]

    def __str__(self):
        return self.label
