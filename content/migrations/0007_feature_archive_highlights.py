from django.db import migrations


def feature_archive_highlights(apps, schema_editor):
    database = schema_editor.connection.alias
    Profile = apps.get_model("content", "Profile")
    Resource = apps.get_model("content", "Resource")
    MediaAppearance = apps.get_model("content", "MediaAppearance")

    Profile.objects.using(database).filter(full_name="Mukasa Moses Bwesige").update(
        experience=(
            "JRS USA’s 2025 profile describes a path from volunteer experience at "
            "Uganda’s national mental health hospital to humanitarian protection "
            "work in South Sudan and the Democratic Republic of the Congo, followed "
            "by a focus on community-based mental health and psychosocial support. "
            "A World Health Organization feature published on 8 October 2025 "
            "identified Mukasa as an Inter-Regional MHPSS Officer at Jesuit Refugee "
            "Service in Uganda. JRS USA’s 2025 profile describes an interregional "
            "MHPSS role for East and South Africa. These are source-dated descriptions, "
            "not a claim about his current position."
        )
    )
    Resource.objects.using(database).filter(
        slug__in=(
            "despair-and-suicide-related-behaviours-palorinya",
            "who-substance-use-empathy-humanitarian-workers",
        )
    ).update(is_featured=True)
    MediaAppearance.objects.using(database).filter(
        slug__in=(
            "suicide-prevention-training-english",
            "suicide-prevention-training-ukrainian",
        )
    ).update(is_featured=True)


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0006_expand_editorial_archive"),
    ]

    operations = [
        migrations.RunPython(feature_archive_highlights, migrations.RunPython.noop),
    ]
