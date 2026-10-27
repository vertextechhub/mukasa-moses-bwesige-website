from django.db import migrations


def add_resource_publishers(apps, schema_editor):
    database = schema_editor.connection.alias
    Resource = apps.get_model("content", "Resource")
    publishers = {
        "coping-mechanisms-after-a-suicide-attempt": "Cambridge University Press & Assessment",
        "who-substance-use-empathy-humanitarian-workers": "World Health Organization",
        "kigali-today-mental-health-peacebuilding-training": "Kigali Today",
        "great-lakes-research-institute": "Great Lakes Research Institute for Mental Health & Wellbeing",
        "unhcr-suicide-prevention-toolkit": "United Nations High Commissioner for Refugees",
        "undp-integrating-mhpss-into-peacebuilding": "United Nations Development Programme",
        "icglr-mhpss-peacebuilding-training-report-uganda": (
            "International Conference on the Great Lakes Region — Regional Training Facility"
        ),
    }
    for slug, publisher in publishers.items():
        Resource.objects.using(database).filter(slug=slug).update(publisher=publisher)


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0011_resource_publisher"),
    ]

    operations = [
        migrations.RunPython(add_resource_publishers, migrations.RunPython.noop),
    ]
