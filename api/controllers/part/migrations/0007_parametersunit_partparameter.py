# Generated by Django 3.0.1 on 2019-12-28 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0006_part_storage"),
    ]

    operations = [
        migrations.CreateModel(
            name="ParametersUnit",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="ex. Ampere", max_length=255, verbose_name="name")),
                ("symbol", models.CharField(blank=True, help_text="ex. A", max_length=255, verbose_name="symbol")),
                ("prefix", models.CharField(blank=True, help_text="ex. μ", max_length=255, verbose_name="prefix")),
                ("description", models.CharField(blank=True, max_length=255, verbose_name="description")),
            ],
            options={
                "verbose_name": "parameter unit",
                "verbose_name_plural": "parameter units",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="PartParameter",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                ("description", models.CharField(blank=True, max_length=255, verbose_name="description")),
                ("value", models.CharField(max_length=255, verbose_name="value")),
                (
                    "part",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="part_parameters",
                        to="part.Part",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="part.ParametersUnit"
                    ),
                ),
            ],
            options={"ordering": ("name",),},
        ),
    ]