# Generated by Django 3.0.1 on 2020-01-01 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("storage", "0003_storagelocation_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="storagelocation",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="storage_locations",
                to="storage.StorageCategory",
            ),
        ),
    ]
