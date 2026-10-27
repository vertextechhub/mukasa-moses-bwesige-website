from django.db import migrations


def align_editorial_content(apps, schema_editor):
    database = schema_editor.connection.alias
    WorkArea = apps.get_model("content", "WorkArea")
    MediaAppearance = apps.get_model("content", "MediaAppearance")
    SourceReference = apps.get_model("content", "SourceReference")

    WorkArea.objects.using(database).filter(
        slug="mental-health-conflict-and-peacebuilding"
    ).update(
        description=(
            "An ARQ interview discusses mental health in conflict zones. "
            "Professional sources also document the relationship between MHPSS and peacebuilding."
        )
    )

    reference, _ = SourceReference.objects.using(database).get_or_create(
        url="https://arq.org/en/news/towards-equitable-collaboration-mhpss",
        defaults={
            "title": "Towards Equitable Collaboration in MHPSS",
            "publisher": "ARQ International",
            "verification_status": "needs_review",
            "notes": "Symposium and video-compilation details supplied in the source register; direct page retrieval failed.",
        },
    )
    appearance, _ = MediaAppearance.objects.using(database).get_or_create(
        slug="towards-equitable-collaboration-in-mhpss",
        defaults={
            "title": "Towards Equitable Collaboration in MHPSS",
            "summary": "ARQ symposium and video-compilation listing; specific contribution and recording details require confirmation.",
            "media_type": "conference",
            "language": "en",
            "source": "ARQ International",
            "source_url": reference.url,
            "original_url": reference.url,
            "published_year": 2025,
            "is_published": False,
            "order": 8,
        },
    )
    appearance.source_references.add(reference)


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0002_insight_is_featured_insight_published_year_and_more"),
    ]

    operations = [
        migrations.RunPython(align_editorial_content, migrations.RunPython.noop),
    ]
