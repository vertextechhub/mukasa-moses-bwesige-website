from django.db import migrations


def publish_contextual_resources(apps, schema_editor):
    database = schema_editor.connection.alias
    Resource = apps.get_model("content", "Resource")
    SourceReference = apps.get_model("content", "SourceReference")
    WorkArea = apps.get_model("content", "WorkArea")

    unhcr_url = "https://www.unhcr.org/uk/sites/uk/files/2023-04/unhcr-suicide-prevention-toolkit_0_1.pdf"
    undp_url = "https://www.undp.org/sites/g/files/zskgke326/files/2022-05/UNDP-Integrating-Mental-Health-and-Psychosocial-Support-into-Peacebuilding-V2.pdf"
    icglr_url = "https://www.icglr-rtf.org/publication/view/mhpss-pb-report-for-uganda-training/"

    unhcr_reference = SourceReference.objects.using(database).get(url=unhcr_url)
    unhcr_reference.notes = (
        "Official UNHCR PDF URL is recorded. The file could not be retrieved during "
        "this check; edition, exact publication date and title-page author/editor "
        "credits remain unverified. Public listing is attributed to UNHCR only."
    )
    unhcr_reference.save(using=database)
    unhcr = Resource.objects.using(database).get(slug="unhcr-suicide-prevention-toolkit")
    unhcr.summary = (
        "UNHCR guidance on planning suicide prevention and risk mitigation in "
        "refugee settings, presented as an institutional resource."
    )
    unhcr.description = (
        "This listing points to UNHCR’s toolkit for multisectoral suicide "
        "prevention and risk mitigation in refugee settings. The official PDF "
        "could not be retrieved during this source check, so edition details, "
        "publication date and title-page credits remain unverified. It is "
        "attributed to UNHCR as an institutional resource; no individual "
        "authorship or editorial role by Mukasa is claimed."
    )
    unhcr.author_credit = ""
    unhcr.source_attribution = (
        "UNHCR; edition and title-page credits require publisher-source confirmation"
    )
    unhcr.is_published = True
    unhcr.save(using=database)
    unhcr.source_references.add(unhcr_reference)

    undp_reference = SourceReference.objects.using(database).get(url=undp_url)
    undp_reference.notes = (
        "Official UNDP report URL and title are recorded in the source register. "
        "The PDF returned HTTP 403 during this check, so detailed bibliographic "
        "metadata and any individual contribution credit are not asserted."
    )
    undp_reference.save(using=database)
    undp = Resource.objects.using(database).get(
        slug="undp-integrating-mhpss-into-peacebuilding"
    )
    undp.summary = (
        "UNDP institutional report on integrating mental health and psychosocial "
        "support into peacebuilding; included as contextual reading only."
    )
    undp.description = (
        "This institutional report is included as contextual reading on MHPSS "
        "and peacebuilding. The source PDF returned HTTP 403 during this check, "
        "so the public listing is limited to the title, publisher and year "
        "recorded in the source register. No individual authorship or contribution "
        "by Mukasa is attributed."
    )
    undp.author_credit = ""
    undp.source_attribution = "United Nations Development Programme (institutional report)"
    undp.is_published = True
    undp.save(using=database)
    undp.source_references.add(undp_reference)

    icglr_reference, _ = SourceReference.objects.using(database).get_or_create(
        url=icglr_url,
        defaults={
            "title": "MHPSS & Peace Building ToT Report, Uganda",
            "publisher": "ICGLR Regional Training Facility",
            "verification_status": "needs_review",
            "notes": (
                "Publisher URL resolves to a PDF. The source dossier identifies "
                "it as the Uganda MHPSS and peacebuilding Training of Trainers "
                "report (January 2025); exact title-page credits were not checked."
            ),
        },
    )
    report, _ = Resource.objects.using(database).get_or_create(
        slug="icglr-mhpss-peacebuilding-training-report-uganda",
        defaults={
            "title": "MHPSS & Peace Building ToT Report, Uganda",
            "summary": (
                "ICGLR Regional Training Facility report on a Uganda Training of "
                "Trainers integrating MHPSS and peacebuilding."
            ),
            "description": (
                "The ICGLR-RTF publication page links to a PDF report about "
                "MHPSS and peacebuilding training in Uganda. The source dossier "
                "records the training in January 2025. Individual report authors "
                "and complete bibliographic metadata have not been confirmed, so "
                "this item is attributed to the institutional publisher and is "
                "not represented as a personal publication."
            ),
            "resource_type": "report",
            "source_attribution": (
                "ICGLR Regional Training Facility (institutional report)"
            ),
            "source_url": icglr_url,
            "published_year": 2025,
            "is_published": True,
            "order": 6,
        },
    )
    report.source_references.add(icglr_reference)

    suicide_area = WorkArea.objects.using(database).filter(
        slug="suicide-prevention-and-research"
    ).first()
    conflict_area = WorkArea.objects.using(database).filter(
        slug="mental-health-conflict-and-peacebuilding"
    ).first()
    if suicide_area:
        unhcr.related_areas.add(suicide_area)
    if conflict_area:
        undp.related_areas.add(conflict_area)
        report.related_areas.add(conflict_area)


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0009_set_kigali_media_language"),
    ]

    operations = [
        migrations.RunPython(publish_contextual_resources, migrations.RunPython.noop),
    ]
