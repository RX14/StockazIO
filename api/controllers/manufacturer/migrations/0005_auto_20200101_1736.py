# Generated by Django 3.0.1 on 2020-01-01 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("manufacturer", "0004_auto_20191230_2127"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="manufacturerlogo",
            options={
                "ordering": ("id",),
                "verbose_name": "Manufacturer Logo",
                "verbose_name_plural": "Manufacturer Logos",
            },
        ),
    ]
