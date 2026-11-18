"""Validate the complete reference rather than accepting a final newline."""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("payments", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="reference",
            field=models.CharField(
                blank=True,
                max_length=30,
                validators=[
                    django.core.validators.RegexValidator(
                        r"\A[A-Za-z0-9]*\Z", "Use letters and numbers only."
                    )
                ],
            ),
        )
    ]
