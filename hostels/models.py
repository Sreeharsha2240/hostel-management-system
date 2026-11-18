from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models, transaction


def _save_update_fields(args, kwargs):
    """Materialize update_fields once, including Django's positional save API."""
    fields = kwargs.get("update_fields", args[3] if len(args) > 3 else None)
    if fields is not None:
        fields = frozenset(fields)
        if len(args) > 3 and "update_fields" not in kwargs:
            args = (*args[:3], fields, *args[4:])
        else:
            kwargs["update_fields"] = fields
    return args, kwargs, fields


class HostelQuerySet(models.QuerySet):
    ELIGIBILITY_FIELDS = {"hostel_type", "is_active"}

    def update(self, **kwargs):
        if self.ELIGIBILITY_FIELDS.intersection(kwargs):
            raise ValueError("Use Hostel.save() to preserve resident eligibility.")
        if "name" in kwargs:
            if hasattr(kwargs["name"], "resolve_expression"):
                raise ValueError("Use Hostel.save() to validate hostel names.")
            kwargs["name"] = self.model._meta.get_field("name").clean(
                kwargs["name"], self.model()
            )
        return super().update(**kwargs)

    def bulk_update(self, objs, fields, batch_size=None):
        fields = tuple(fields)
        if self.ELIGIBILITY_FIELDS.intersection(fields) or "name" in fields:
            raise ValueError("Use Hostel.save() to preserve resident eligibility.")
        return super().bulk_update(objs, fields, batch_size=batch_size)

    def bulk_create(
        self,
        objs,
        batch_size=None,
        ignore_conflicts=False,
        update_conflicts=False,
        update_fields=None,
        unique_fields=None,
    ):
        # Upserts also bypass save() on existing hostels.
        if update_conflicts:
            raise ValueError("Use Hostel.save() to preserve resident eligibility.")
        objs = list(objs)
        for obj in objs:
            for name in ("name", "hostel_type", "is_active"):
                setattr(
                    obj,
                    name,
                    self.model._meta.get_field(name).clean(getattr(obj, name), obj),
                )
        return super().bulk_create(
            objs,
            batch_size=batch_size,
            ignore_conflicts=ignore_conflicts,
            update_conflicts=update_conflicts,
            update_fields=update_fields,
            unique_fields=unique_fields,
        )


class Hostel(models.Model):
    objects = HostelQuerySet.as_manager()

    class HostelType(models.TextChoices):
        BOYS = "Boys", "Boys"
        GIRLS = "Girls", "Girls"

    # Keep the original storage width so migrations never truncate legacy data.
    name = models.CharField(
        max_length=100, unique=True, validators=[MaxLengthValidator(40)]
    )
    hostel_type = models.CharField(max_length=5, choices=HostelType.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def _validate_active_residents(self, *, hostel_type=None, is_active=None):
        from allocations.models import Allocation
        from students.models import Student

        active_allocations = Allocation.objects.filter(
            bed__room__hostel_id=self.pk,
            status=Allocation.AllocationStatus.ACTIVE,
        )

        hostel_type = self.hostel_type if hostel_type is None else hostel_type
        is_active = self.is_active if is_active is None else is_active
        if not is_active and active_allocations.exists():
            raise ValidationError(
                {
                    "is_active": (
                        "This hostel cannot be deactivated while it has "
                        "active resident allocations."
                    )
                }
            )

        expected_gender = {
            self.HostelType.BOYS: Student.Gender.MALE,
            self.HostelType.GIRLS: Student.Gender.FEMALE,
        }.get(hostel_type)

        if (
            expected_gender
            and active_allocations.exclude(student__gender=expected_gender).exists()
        ):
            raise ValidationError(
                {
                    "hostel_type": (
                        "The hostel type cannot be changed because active "
                        "residents would become ineligible."
                    )
                }
            )

    def clean(self):
        super().clean()

        if self.pk:
            self._validate_active_residents()

    @transaction.atomic
    def save(self, *args, **kwargs):
        args, kwargs, update_fields = _save_update_fields(args, kwargs)
        if update_fields is not None and not update_fields:
            return
        for field in HostelQuerySet.ELIGIBILITY_FIELDS | {"name"}:
            if update_fields is None or field in update_fields:
                try:
                    setattr(
                        self,
                        field,
                        self._meta.get_field(field).clean(getattr(self, field), self),
                    )
                except ValidationError as error:
                    raise ValidationError({field: error.messages}) from error
        if self.pk and (
            update_fields is None
            or HostelQuerySet.ELIGIBILITY_FIELDS.intersection(update_fields)
        ):
            # Room creation/moves lock their target hostel before locking a room.
            # Holding the hostel row makes this room set stable while we lock it.
            previous = Hostel.objects.select_for_update().get(pk=self.pk)
            list(
                Room.objects.select_for_update()
                .filter(hostel_id=self.pk)
                .order_by("pk")
                .values_list("pk", flat=True)
            )
            self._validate_active_residents(
                hostel_type=(
                    self.hostel_type
                    if update_fields is None or "hostel_type" in update_fields
                    else previous.hostel_type
                ),
                is_active=(
                    self.is_active
                    if update_fields is None or "is_active" in update_fields
                    else previous.is_active
                ),
            )
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RoomQuerySet(models.QuerySet):
    SYNC_FIELDS = {"capacity", "room_number"}
    PROTECTED_FIELDS = SYNC_FIELDS | {"hostel", "hostel_id"}

    def update(self, **kwargs):
        if self.PROTECTED_FIELDS.intersection(kwargs):
            raise ValueError(
                "Use Room.save() to change capacity, room_number, or hostel "
                "so room and bed history can be checked."
            )
        if "floor" in kwargs:
            kwargs["floor"] = self.model._meta.get_field("floor").clean(
                kwargs["floor"], self.model()
            )
        return super().update(**kwargs)

    def bulk_update(self, objs, fields, batch_size=None):
        fields = tuple(fields)
        if self.PROTECTED_FIELDS.intersection(fields) or "floor" in fields:
            raise ValueError(
                "Use Room.save() to change capacity, room_number, or hostel "
                "so room and bed history can be checked."
            )
        return super().bulk_update(objs, fields, batch_size=batch_size)

    def bulk_create(self, *args, **kwargs):
        raise ValueError("Use Room.save() to create and synchronize room beds.")


class Room(models.Model):
    objects = RoomQuerySet.as_manager()

    class RoomType(models.TextChoices):
        SINGLE = "Single", "Single"
        DOUBLE = "Double", "Double"
        TRIPLE = "Triple", "Triple"

    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.PROTECT,
        related_name="rooms",
    )
    room_number = models.CharField(
        max_length=10,
        validators=[
            MaxLengthValidator(6),
            RegexValidator(
                r"\A[A-Za-z0-9]{1,6}\Z", "Enter 1 to 6 alphanumeric characters."
            ),
        ],
    )
    floor = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)])
    room_type = models.CharField(max_length=10, choices=RoomType.choices)
    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    fee_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Room fee in INR. Set a positive fee before using payment status.",
    )

    class Meta:
        ordering = ["hostel", "floor", "room_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["hostel", "room_number"],
                name="unique_room_number_per_hostel",
            ),
            models.CheckConstraint(
                condition=models.Q(fee_amount__gte=0),
                name="nonnegative_room_fee",
            ),
        ]

    def _validate_active_resident_eligibility(self, hostel_id):
        """Reject moves that make active residents ineligible."""
        from allocations.models import Allocation
        from students.models import Student

        target_hostel = (
            Hostel.objects.filter(pk=hostel_id)
            .values("hostel_type", "is_active")
            .first()
        )

        if target_hostel is None:
            return

        active_allocations = Allocation.objects.filter(
            bed__room_id=self.pk,
            status=Allocation.AllocationStatus.ACTIVE,
        )

        if not active_allocations.exists():
            return

        if not target_hostel["is_active"]:
            raise ValidationError(
                {
                    "hostel": (
                        "This room cannot be moved to an inactive hostel while "
                        "it has active residents."
                    )
                }
            )

        expected_gender = {
            Hostel.HostelType.BOYS: Student.Gender.MALE,
            Hostel.HostelType.GIRLS: Student.Gender.FEMALE,
        }.get(target_hostel["hostel_type"])

        if expected_gender is None:
            return

        if active_allocations.exclude(student__gender=expected_gender).exists():
            raise ValidationError(
                {
                    "hostel": (
                        "This room cannot be moved to the selected hostel because "
                        "it has active residents whose gender is incompatible. "
                        "Transfer or complete their allocations first."
                    )
                }
            )

    def clean(self):
        super().clean()

        if self.capacity is not None:
            try:
                self.capacity = self._meta.get_field("capacity").clean(
                    self.capacity, self
                )
            except ValidationError as error:
                raise ValidationError({"capacity": error.messages}) from error

        if not self.pk:
            return

        from allocations.models import Allocation

        if self.hostel_id is not None:
            previous_hostel_id = (
                Room.objects.filter(pk=self.pk)
                .values_list("hostel_id", flat=True)
                .first()
            )
            if (
                previous_hostel_id is not None
                and previous_hostel_id != self.hostel_id
                and self.beds.filter(allocations__isnull=False).exists()
            ):
                raise ValidationError(
                    {
                        "hostel": "A room with allocation history cannot be moved "
                        "to another hostel; that would rewrite historical location."
                    }
                )

        if self.capacity is not None:
            allocated_beds = (
                self.beds.filter(allocations__status=Allocation.AllocationStatus.ACTIVE)
                .distinct()
                .count()
            )

            if allocated_beds > self.capacity:
                raise ValidationError(
                    {
                        "capacity": (
                            f"This room has {allocated_beds} beds with active "
                            "allocations. Complete or move allocations before "
                            "reducing capacity further."
                        )
                    }
                )

    @transaction.atomic
    def save(self, *args, **kwargs):
        args, kwargs, update_fields = _save_update_fields(args, kwargs)
        if update_fields is not None and not update_fields:
            return

        old_room_number = None
        room_number = self.room_number
        capacity = self.capacity

        for field in ("room_number", "floor", "fee_amount"):
            if update_fields is None or field in update_fields:
                try:
                    setattr(
                        self,
                        field,
                        self._meta.get_field(field).clean(getattr(self, field), self),
                    )
                except ValidationError as error:
                    raise ValidationError({field: error.messages}) from error

        if update_fields is None or "capacity" in update_fields:
            try:
                self.capacity = self._meta.get_field("capacity").clean(
                    self.capacity, self
                )
            except ValidationError as error:
                raise ValidationError({"capacity": error.messages}) from error
            capacity = self.capacity

        hostel_is_being_saved = update_fields is None or bool(
            {"hostel", "hostel_id"}.intersection(update_fields)
        )
        if hostel_is_being_saved and self.hostel_id is not None:
            # Serialize entry into a hostel with deactivation/type changes.
            Hostel.objects.select_for_update().get(pk=self.hostel_id)

        if self.pk:
            previous = Room.objects.select_for_update().get(pk=self.pk)
            old_room_number = previous.room_number

            if update_fields is not None:
                if "room_number" not in update_fields:
                    room_number = previous.room_number

                if "capacity" not in update_fields:
                    capacity = previous.capacity
            if (
                hostel_is_being_saved
                and previous.hostel_id != self.hostel_id
                and self.beds.filter(allocations__isnull=False).exists()
            ):
                raise ValidationError(
                    {
                        "hostel": (
                            "A room with allocation history cannot be moved to "
                            "another hostel; that would rewrite historical location."
                        )
                    }
                )

            if hostel_is_being_saved and previous.hostel_id != self.hostel_id:
                self._validate_active_resident_eligibility(self.hostel_id)

        super().save(*args, **kwargs)

        if update_fields is not None and not RoomQuerySet.SYNC_FIELDS.intersection(
            update_fields
        ):
            return

        # Rename existing bed labels when the room number changes.
        if old_room_number is not None and old_room_number != room_number:
            for bed in self.beds.select_for_update().order_by("pk"):
                suffix = bed.label.rsplit("-", 1)[-1]
                bed.label = f"{room_number}-{suffix}"
                bed.save(update_fields=["label"])

        # Remove excess beds only when they have no allocation history.
        if self.beds.count() > capacity:
            removable_beds = (
                self.beds.exclude(allocations__isnull=False)
                .order_by("-label")
                .distinct()
            )

            excess = self.beds.count() - capacity

            for bed in removable_beds[:excess]:
                bed.delete()

        # Create missing beds without duplicating existing labels.
        for suffix in ["A", "B", "C", "D"][:capacity]:
            Bed.objects.get_or_create(
                room=self,
                label=f"{room_number}-{suffix}",
                defaults={"status": Bed.BedStatus.AVAILABLE},
            )

        # Never silently delete a bed with allocation history.
        if self.beds.count() > capacity:
            from allocations.models import Allocation

            active_bed_count = (
                self.beds.filter(allocations__status=Allocation.AllocationStatus.ACTIVE)
                .distinct()
                .count()
            )

            if active_bed_count > capacity:
                raise ValidationError(
                    "Capacity cannot be reduced below the number of "
                    "beds with active allocations."
                )

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"


class BedQuerySet(models.QuerySet):
    ROOM_FIELDS = {"room", "room_id", "status", "label"}

    def update(self, **kwargs):
        if self.ROOM_FIELDS.intersection(kwargs):
            raise ValueError(
                "Use Bed.save() to change a bed's room or status so allocation history "
                "can be checked."
            )
        return super().update(**kwargs)

    def bulk_update(self, objs, fields, batch_size=None):
        fields = tuple(fields)
        if self.ROOM_FIELDS.intersection(fields):
            raise ValueError(
                "Use Bed.save() to change a bed's room or status so allocation history "
                "can be checked."
            )
        return super().bulk_update(objs, fields, batch_size=batch_size)

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
            raise ValueError("Use Bed.save() to preserve room and allocation history.")
        objs = list(objs)
        for obj in objs:
            for name in ("label", "status"):
                setattr(
                    obj,
                    name,
                    self.model._meta.get_field(name).clean(getattr(obj, name), obj),
                )
        return super().bulk_create(
            objs,
            batch_size=batch_size,
            ignore_conflicts=ignore_conflicts,
            update_conflicts=update_conflicts,
            update_fields=update_fields,
            unique_fields=unique_fields,
        )


class Bed(models.Model):
    objects = BedQuerySet.as_manager()

    class BedStatus(models.TextChoices):
        AVAILABLE = "Available", "Available"
        OCCUPIED = "Occupied", "Occupied"
        MAINTENANCE = "Maintenance", "Under maintenance"

    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="beds",
    )
    label = models.CharField(max_length=20, validators=[MaxLengthValidator(8)])
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

    def _validate_active_status(self):
        from allocations.models import Allocation

        if self.pk and self.status == self.BedStatus.AVAILABLE:
            if Allocation.objects.filter(
                bed_id=self.pk, status=Allocation.AllocationStatus.ACTIVE
            ).exists():
                raise ValidationError(
                    {
                        "status": "A bed with an active allocation cannot be marked Available. "
                        "Release or transfer the resident first."
                    }
                )

    def clean(self):
        super().clean()
        errors = {}
        try:
            self._validate_active_status()
        except ValidationError as error:
            errors.update(error.message_dict)
        if self.pk and self.room_id is not None:
            previous_room_id = (
                type(self)
                .objects.filter(pk=self.pk)
                .values_list("room_id", flat=True)
                .first()
            )
            if previous_room_id is not None and previous_room_id != self.room_id:
                from allocations.models import Allocation

                if Allocation.objects.filter(bed_id=self.pk).exists():
                    errors["room"] = (
                        "A bed with allocation history cannot be moved to another "
                        "room; that would rewrite historical location."
                    )
        if errors:
            raise ValidationError(errors)

    @transaction.atomic
    def save(self, *args, **kwargs):
        args, kwargs, update_fields = _save_update_fields(args, kwargs)
        if update_fields is not None and not update_fields:
            return
        room_is_being_saved = update_fields is None or bool(
            {"room", "room_id"}.intersection(update_fields)
        )
        status_is_being_saved = update_fields is None or "status" in update_fields
        if update_fields is None or "label" in update_fields:
            try:
                self.label = self._meta.get_field("label").clean(self.label, self)
            except ValidationError as error:
                raise ValidationError({"label": error.messages}) from error
        if status_is_being_saved:
            try:
                self.status = self._meta.get_field("status").clean(self.status, self)
            except ValidationError as error:
                raise ValidationError({"status": error.messages}) from error
        if self.pk and (room_is_being_saved or status_is_being_saved):
            previous_room_id = (
                type(self)
                .objects.filter(pk=self.pk)
                .values_list("room_id", flat=True)
                .first()
            )
            if previous_room_id is not None:
                # Allocation and inventory edits share Room -> Bed lock order.
                # Never take a Hostel lock here: allocation already holds Rooms.
                room_ids = {previous_room_id}
                if room_is_being_saved and self.room_id is not None:
                    room_ids.add(self.room_id)
                list(
                    Room.objects.select_for_update()
                    .filter(pk__in=sorted(room_ids))
                    .order_by("pk")
                    .values_list("pk", flat=True)
                )
                try:
                    previous = type(self).objects.select_for_update().get(pk=self.pk)
                except type(self).DoesNotExist:
                    raise ValidationError(
                        "This bed no longer exists. Refresh and try again."
                    ) from None
                if previous.room_id != previous_room_id:
                    raise ValidationError(
                        "This bed's room changed. Refresh and try again."
                    )
                if room_is_being_saved and previous.room_id != self.room_id:
                    from allocations.models import Allocation

                    if Allocation.objects.filter(bed_id=self.pk).exists():
                        raise ValidationError(
                            {
                                "room": "A bed with allocation history cannot be moved "
                                "to another room; that would rewrite historical location."
                            }
                        )
                if status_is_being_saved:
                    self._validate_active_status()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.label
