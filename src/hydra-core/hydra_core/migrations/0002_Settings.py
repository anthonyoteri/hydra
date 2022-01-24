# Generated by Django 4.0.1 on 2022-01-12 00:02

from django.db import migrations, models
from django_add_default_value import AddDefaultValue


def create_initial_settings(apps, schema_editor):
    Settings = apps.get_model("hydra_core", "Settings")
    Settings().save()


class Migration(migrations.Migration):

    dependencies = [
        ('hydra_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('retention_period_days', models.IntegerField(default=360)),
                ('align_timestamps', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        AddDefaultValue(model_name="Settings", name="retention_period_days", value=360),
        AddDefaultValue(model_name="Settings", name="align_timestamps", value=False),
        migrations.RunPython(create_initial_settings)
    ]