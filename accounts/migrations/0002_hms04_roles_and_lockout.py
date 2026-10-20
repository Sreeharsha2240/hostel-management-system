from django.db import migrations, models


def mark_existing_superusers_as_admin(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    User.objects.filter(is_superuser=True).update(role='admin')


class Migration(migrations.Migration):
    dependencies = [('accounts', '0001_initial')]

    operations = [
        migrations.AddField(
            model_name='user', name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('warden', 'Warden'), ('student', 'Student')], default='student', max_length=16),
        ),
        migrations.AddField(
            model_name='user', name='failed_attempts',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user', name='locked_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunPython(mark_existing_superusers_as_admin, migrations.RunPython.noop),
    ]
