# Generated by Django 3.2.2 on 2021-05-09 06:42

from django.db import migrations


def dedup_table(apps, schema_editor):
    # Get model
    ParametersUnit = apps.get_model("part", "ParametersUnit")
    PartParameter = apps.get_model("part", "PartParameter")

    # For each PartParameter, reassociate its unit
    for pp in PartParameter.objects.all():
        if not pp.unit:
            continue

        # Reassociate pp.unit to the first found ParametersUnit ordered by ID
        pu = ParametersUnit.objects.order_by("id").filter(name=pp.unit.name).first()
        if not pu:
            print(f"Cannot find a ParametersUnit with name={pp.unit.name}")
            continue
        pp.unit = pu
        pp.save()

    pu_values = ParametersUnit.objects.values("name").distinct()
    for value in pu_values:
        # Get first matching ParametersUnit, others will be dropped
        pu = ParametersUnit.objects.order_by("id").filter(name=value["name"]).first()
        # Delete entries with the same name, excluding the first one with ID
        ParametersUnit.objects.filter(name=pu.name).exclude(id=pu.id).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0020_alter_partparameterpresetitem_part_parameter_preset"),
    ]

    operations = [migrations.RunPython(dedup_table)]
