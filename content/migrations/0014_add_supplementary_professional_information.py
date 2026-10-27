from django.db import migrations


def add_supplementary_professional_information(apps, schema_editor):
    database = schema_editor.connection.alias
    Experience = apps.get_model("content", "ProfessionalExperience")
    Resource = apps.get_model("content", "Resource")

    role_title = "Global Mission Transformation – Protection Specialist"
    role_organization = "Jesuit Refugee Service (JRS)"
    if not Experience.objects.using(database).filter(
        title__iexact=role_title,
        organization__iexact=role_organization,
    ).exists():
        Experience.objects.using(database).create(
            title=role_title,
            organization=role_organization,
            location="Global Virtual Office, Global Mission Transformation Unit",
            experience_type="employment",
            description=(
                "Additional professional appointment supplied for this update. "
                "No appointment dates were supplied."
            ),
            evidence_status="profile_dossier",
            evidence_note="Appointment details supplied for this update; no dates supplied.",
            sort_order=19,
            is_featured=True,
            is_published=True,
        )

    resources = (
        {
            "slug": "culture-context-mental-health-south-sudan-displacement",
            "title": (
                "Culture, Context and Mental Health and Psychosocial Well-being "
                "of Refugees and Internally Displaced Persons from South Sudan"
            ),
            "resource_type": "report",
            "published_year": 2023,
            "publisher": "United Nations High Commissioner for Refugees",
            "description": (
                "Institutional publication. Individual authorship or contribution "
                "is not attributed in the information supplied."
            ),
        },
        {
            "slug": "treatment-outcomes-substance-use-disorders-africa",
            "title": (
                "Treatment Outcomes for Substance Use Disorders Across the African "
                "Continent: A Systematic Review"
            ),
            "resource_type": "research",
            "published_year": 2025,
            "journal_name": "BMC Psychology",
            "description": (
                "Individual authorship or contribution is not specified in the "
                "information supplied."
            ),
        },
        {
            "slug": "integrating-mhpss-peacebuilding-programs-practical-guide",
            "title": "Integrating MHPSS into Peacebuilding Programs: A Practical Guide",
            "resource_type": "toolkit",
            "published_year": 2025,
            "description": (
                "Individual authorship or contribution is not specified in the "
                "information supplied."
            ),
        },
        {
            "slug": "reflexive-training-reimagining-trainers-of-trainers",
            "title": (
                "Reflexive Training: Reimagining Trainers of Trainers in Mental "
                "Health and Psychosocial Support"
            ),
            "resource_type": "other",
            "author_credit": "Moses Mukasa Bwesige",
            "description": (
                "The book challenges foundational assumptions in Training of "
                "Trainers (ToT) practice in MHPSS. Drawing on critical pedagogy, "
                "anthropology and reflexive practice, it presents reflexive training "
                "as an ethical and political practice."
            ),
        },
    )

    for resource in resources:
        title = resource["title"]
        if not Resource.objects.using(database).filter(title__iexact=title).exists():
            Resource.objects.using(database).create(
                slug=resource.pop("slug"),
                **resource,
                is_published=True,
            )


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0013_professional_experience"),
    ]

    operations = [
        migrations.RunPython(
            add_supplementary_professional_information,
            migrations.RunPython.noop,
        ),
    ]
