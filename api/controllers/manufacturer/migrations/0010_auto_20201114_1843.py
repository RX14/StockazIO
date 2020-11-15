# Generated by Django 3.1.3 on 2020-11-14 18:43

# migrate from a one-to-many to a well, no relations at all

from django.db import migrations
from os import path


def move_logo_to_parent(apps, schema_editor):
    """
    Move manufacturer.logos[0].logo to manufacturer.logo
    """
    Manufacturer = apps.get_model("manufacturer", "Manufacturer")
    for manufacturer in Manufacturer.objects.all():
        logo = manufacturer.logos.first()
        if logo:
            # continues only if we have a logo
            manufacturer.logo.save(path.basename(logo.logo.name), logo.logo.file, save=False)
            manufacturer.save()


class Migration(migrations.Migration):

    dependencies = [
        ("manufacturer", "0009_manufacturer_logo"),
    ]

    operations = [migrations.RunPython(move_logo_to_parent)]