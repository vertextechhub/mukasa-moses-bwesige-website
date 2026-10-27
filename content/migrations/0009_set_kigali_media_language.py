from django.db import migrations


def set_kigali_language(apps, schema_editor):
    database = schema_editor.connection.alias
    MediaAppearance = apps.get_model("content", "MediaAppearance")
    Resource = apps.get_model("content", "Resource")

    MediaAppearance.objects.using(database).filter(
        slug="kigali-today-mental-health-peacebuilding-training"
    ).update(language="rw")
    Resource.objects.using(database).filter(
        slug="kigali-today-mental-health-peacebuilding-training"
    ).update(language="Kinyarwanda")


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0008_alter_mediaappearance_language"),
    ]

    operations = [
        migrations.RunPython(set_kigali_language, migrations.RunPython.noop),
    ]
