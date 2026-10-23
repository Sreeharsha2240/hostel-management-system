
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone


class Allocation(models.Model):
    class AllocationStatus(models.TextChoices):
        ACTIVE = "Active", "Active"
        COMPLETED = "Completed", "Completed"
        CANCELLED = "Cancelled", "Cancelled"

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.PROTECT,
        related_name="allocations",
    )
    bed = models.ForeignKey(
        "hostels.Bed",
        on_delete=models.PROTECT,
        related_name="allocations",
    )
    allocated_on = models.DateField(default=timezone.localdate)
    vacated_on = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=AllocationStatus.choices,
        default=AllocationStatus.ACTIVE,
    )

    # These fields contain IDs only while the allocation is active.
    # MySQL can enforce ordinary unique constraints on them.
    active_student_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        unique=True,
        editable=False,
    )
    active_bed_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        unique=True,
        editable=False,
    )

    class Meta:
        ordering = ["-allocated_on"]

    def clean(self):
        super().clean()

        if self.vacated_on and self.vacated_on < self.allocated_on:
            raise ValidationError({
                "vacated_on": "Vacated date cannot be before the allocation date."
            })

        if self.status == self.AllocationStatus.ACTIVE and self.vacated_on:
            raise ValidationError({
                "vacated_on": "An active allocation cannot have a vacated date."
            })

    @transaction.atomic
    def save(self, *args, **kwargs):
        previous = None

        if self.pk:
            previous = (
                Allocation.objects.select_for_update()
                .filter(pk=self.pk)
                .first()
            )

        self.full_clean()

        if self.status == self.AllocationStatus.ACTIVE:
            if self.bed.status == "Maintenance":
                raise ValidationError(
                    "A bed under maintenance cannot be allocated."
                )

            if Allocation.objects.filter(
                student_id=self.student_id,
                status=self.AllocationStatus.ACTIVE,
            ).exclude(pk=self.pk).exists():
                raise ValidationError(
                    "This student already has an active allocation."
                )

            if Allocation.objects.filter(
                bed_id=self.bed_id,
                status=self.AllocationStatus.ACTIVE,
            ).exclude(pk=self.pk).exists():
                raise ValidationError(
                    "This bed already has an active allocation."
                )

            self.active_student_id = self.student_id
            self.active_bed_id = self.bed_id
        else:
            self.active_student_id = None
            self.active_bed_id = None

        super().save(*args, **kwargs)

        if previous and previous.status == self.AllocationStatus.ACTIVE:
            if (
                previous.bed_id != self.bed_id
                or self.status != self.AllocationStatus.ACTIVE
            ):
                old_bed = previous.bed
                if old_bed.status == "Occupied":
                    old_bed.status = "Available"
                    old_bed.save(update_fields=["status"])

        if self.status == self.AllocationStatus.ACTIVE:
            bed = self.bed
            if bed.status != "Occupied":
                bed.status = "Occupied"
                bed.save(update_fields=["status"])

    def __str__(self):
        return f"{self.student.student_id} - {self.bed.label} ({self.status})"
