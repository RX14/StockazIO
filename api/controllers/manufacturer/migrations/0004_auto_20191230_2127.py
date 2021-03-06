# Generated by Django 3.0.1 on 2019-12-30 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("manufacturer", "0003_auto_20191230_1302"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="manufacturer",
            options={"ordering": ("name",), "verbose_name": "Manufacturer", "verbose_name_plural": "Manufacturers"},
        ),
        migrations.AlterModelOptions(
            name="manufacturerlogo",
            options={
                "ordering": ("id",),
                "verbose_name": "Manufacturer Logo",
                "verbose_name_plural": "Manufacturers Logo",
            },
        ),
        migrations.AlterModelOptions(
            name="partmanufacturer",
            options={
                "ordering": ("sku",),
                "verbose_name": "Part Manufacturer",
                "verbose_name_plural": "Part Manufacturers",
            },
        ),
    ]
