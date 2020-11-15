# Generated by Django 3.1.3 on 2020-11-14 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manufacturer", "0008_auto_20201114_1636"),
    ]

    operations = [
        migrations.AddField(
            model_name="manufacturer",
            name="logo",
            field=models.ImageField(
                blank=True, null=True, upload_to="manufacturers/", verbose_name="Manufacturer logo"
            ),
        ),
    ]