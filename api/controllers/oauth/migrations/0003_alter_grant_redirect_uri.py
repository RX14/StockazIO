# Generated by Django 3.2.2 on 2021-05-08 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oauth", "0002_auto_20201026_1400"),
    ]

    operations = [
        migrations.AlterField(
            model_name="grant",
            name="redirect_uri",
            field=models.TextField(),
        ),
    ]