from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [('accounts', '0002_hms04_roles_and_lockout')]

    operations = [
        migrations.CreateModel(
            name='AuditEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(db_index=True, max_length=40)),
                ('record_type', models.CharField(blank=True, max_length=80)),
                ('record_id', models.CharField(blank=True, max_length=80)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audit_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ('-timestamp',)},
        ),
    ]
