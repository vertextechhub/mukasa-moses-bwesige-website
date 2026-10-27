import datetime

from django.db import migrations


def enrich_verified_media_archive(apps, schema_editor):
    database = schema_editor.connection.alias
    MediaAppearance = apps.get_model("content", "MediaAppearance")

    updates = {
        "lets-talk-life-understanding-suicide-mental-wellness": {
            "title": (
                "Let's talk life - Understanding Suicide and Promoting Mental "
                "Wellness with Mukasa Moses Bwesige"
            ),
        },
        "suicide-prevention-training-english": {
            "title": "Webinar on Suicide prevention [09.04.2025, ENG]",
            "summary": (
                "English-language recording of the suicide-prevention webinar "
                "published by MHPSS TWG Ukraine."
            ),
            "description": (
                "The YouTube title identifies this as the English-language "
                "suicide-prevention webinar dated 9 April 2025. ARQ International's "
                "announcement identifies Mukasa as the trainer for the session. "
                "The recording is published by MHPSS TWG Ukraine."
            ),
            "source": "MHPSS TWG Ukraine",
            "published_on": datetime.date(2025, 4, 9),
            "published_year": 2025,
        },
        "suicide-prevention-training-ukrainian": {
            "title": "Вебінар: «Запобігання самогубствам» [09.04.2025, UKR]",
            "summary": (
                "Ukrainian-language recording of the suicide-prevention webinar "
                "published by MHPSS TWG Ukraine."
            ),
            "description": (
                "The YouTube title identifies this as the Ukrainian-language "
                "suicide-prevention webinar dated 9 April 2025. ARQ International's "
                "announcement identifies Mukasa as the trainer for the session. "
                "The recording is published by MHPSS TWG Ukraine."
            ),
            "source": "MHPSS TWG Ukraine",
            "published_on": datetime.date(2025, 4, 9),
            "published_year": 2025,
        },
        "jrs-insider-centering-mental-health": {
            "title": (
                "JRS Insider: Moses Mukasa on Centering Mental Health in "
                "Refugee Response"
            ),
            "media_type": "feature",
            "summary": (
                "Jesuit Refugee Service USA written profile on centering mental "
                "health in refugee response."
            ),
            "description": (
                "JRS USA's profile recounts Mukasa's path into humanitarian work "
                "and describes community-based and community-led support for "
                "displaced people. The page contains an article and photographs; "
                "no video or embedded recording was found."
            ),
        },
    }

    for slug, values in updates.items():
        MediaAppearance.objects.using(database).filter(slug=slug).update(**values)

    source_url = (
        "https://app.mhpss.net/"
        "webinar-02-this-much-i-know-practitioners-reflect-on-community-based-mhpss"
    )
    item = MediaAppearance.objects.using(database).filter(
        original_url=source_url
    ).first()
    if item is None:
        item = MediaAppearance.objects.using(database).create(
            slug="this-much-i-know-community-based-mhpss",
            title="This Much I Know: Practitioners Reflect on Community-Based MHPSS",
            summary=(
                "MHPSS Network source page for a conversation with Moses Mukasa "
                "about community-based MHPSS."
            ),
            description=(
                "The source page describes a conversation with Moses Mukasa. It "
                "returned HTTP 403 during verification, and no separate public "
                "recording could be confirmed. This entry links to the source "
                "page only and does not embed or label it as a recording."
            ),
            source_url=source_url,
            is_published=True,
            media_type="webinar",
            source="MHPSS Network",
            original_url=source_url,
            language="en",
        )


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0015_add_cv_profile_details"),
    ]

    operations = [
        migrations.RunPython(
            enrich_verified_media_archive,
            migrations.RunPython.noop,
        ),
    ]
