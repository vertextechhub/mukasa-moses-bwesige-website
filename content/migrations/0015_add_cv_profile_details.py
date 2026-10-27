from django.db import migrations


def add_cv_profile_details(apps, schema_editor):
    database = schema_editor.connection.alias
    Experience = apps.get_model("content", "ProfessionalExperience")
    Resource = apps.get_model("content", "Resource")

    def append_experience_details(title, organization, details):
        experience = (
            Experience.objects.using(database)
            .filter(title=title, organization=organization, is_published=True)
            .first()
        )
        if experience and "CV-supplied supplementary details:" not in experience.description:
            experience.description = (
                f"{experience.description}\n\n" if experience.description else ""
            ) + "CV-supplied supplementary details:\n" + details
            experience.save(using=database, update_fields=("description",))

    def add_experience(title, organization, start_year=None, start_month=None,
                       end_year=None, end_month=None, period_note="", location="",
                       experience_type="consultancy", description="", sort_order=30):
        if Experience.objects.using(database).filter(
            title__iexact=title,
            organization__iexact=organization,
        ).exists():
            return
        Experience.objects.using(database).create(
            title=title,
            organization=organization,
            location=location,
            experience_type=experience_type,
            start_year=start_year,
            start_month=start_month,
            end_year=end_year,
            end_month=end_month,
            period_note=period_note,
            description=description,
            evidence_status="profile_dossier",
            evidence_note="Supplementary details supplied in the CV; dates shown only where provided.",
            sort_order=sort_order,
            is_published=True,
        )

    append_experience_details(
        "Global Mission-Oriented Transformation Protection Technical Specialist",
        "Jesuit Refugee Service (JRS)",
        "CV title and period: Protection Technical Specialist, Global Mission-Oriented "
        "Transformation (GMT), June 2026–Present.\n"
        "Supports a coherent, rights-based protection and inclusion framework connecting "
        "global priorities with country-level realities; contributes to practical tools "
        "for protection mainstreaming, risk prevention and mitigation, programme "
        "integration, research and knowledge sharing; bridges programme and advocacy "
        "perspectives; and supports operational learning for organisational "
        "communications and decision-making.",
    )
    append_experience_details(
        "Inter-Regional MHPSS Officer — East & Southern Africa",
        "Jesuit Refugee Service (JRS)",
        "CV period: April 2023–Present. This differs from the existing website record, "
        "which gives January 2023–July 2026 based on the supplied profile chronology "
        "and notes a separate April 2023 source date. The CV lists this role as current "
        "alongside the GMT appointment; the relationship between the appointments is "
        "not established.\n"
        "Provides regional technical advice to directors, country programme officers "
        "and MHPSS teams across 14 countries; supports strategic alignment, programme "
        "review and quality improvement across humanitarian-development-peace "
        "approaches; engages institutional and government stakeholders; contributes "
        "to coordination forums and referral pathways; and supports recruitment, "
        "staff development and capacity strengthening.",
    )
    append_experience_details(
        "Country Program MHPSS Specialist",
        "Lutheran World Federation (LWF)",
        "CV title and period: Country Programme MHPSS and Peacebuilding Technical "
        "Specialist, January 2022–April 2023. The existing website chronology records "
        "July 2022–March 2023; neither date range has been changed.\n"
        "Developed and reviewed harmonised MHPSS frameworks and community-based "
        "psychosocial support approaches for refugee operations. Coordinated the "
        "Mutual and Inter-Related Resilience Programme (€1 million) and COMPASS pilot "
        "project (€1.8 million). Supported strategy design, service mapping, programme "
        "quality, partner coordination and staff capacity building, and helped "
        "mainstream MHPSS into other sectors, including water, sanitation and hygiene "
        "(WASH).",
    )
    append_experience_details(
        "Psychosocial Officer — Northern Uganda refugee emergency",
        "Lutheran World Federation (LWF)",
        "CV title and period: Project Officer, Psychosocial, 2017–2019. The existing "
        "website chronology separately records a Psychosocial Officer period through "
        "May 2022 and a Senior Psychosocial Support Officer entry from January 2019; "
        "the CV does not resolve that overlap.\n"
        "Led harmonised MHPSS approaches and action plans for refugee operations "
        "alongside partners and government stakeholders; designed community-based "
        "support approaches; coached staff and monitored intervention quality; "
        "supervised donor-funded activities; and contributed to proposals, budgets, "
        "needs assessments and peacebuilding.",
    )
    append_experience_details(
        "Public Health — MHPSS / Non-Communicable Diseases",
        "UNHCR Headquarters",
        "CV period: September 2021–April 2022. The existing website chronology ends "
        "in May 2022; this CV period is recorded as a supplementary source detail.\n"
        "Reviewed refugee MHPSS and non-communicable disease programming and its links "
        "with national health systems; developed tools for data analysis and "
        "visualisation; supported interagency coordination and technical guidance; "
        "and contributed to UNHCR’s suicide prevention toolkit and related "
        "operational guidance.",
    )
    append_experience_details(
        "Director of Uganda Operations / Country Representative",
        "Simbi Foundation (Canada)",
        "The CV describes the position as Director of Uganda Operations in 2016; the "
        "existing website record gives March 2015–December 2016 and a different "
        "combined title. The source-page identity caveat remains applicable.\n"
        "Led Uganda operations, recruitment, staff management and performance "
        "processes; supported field teams in Bidibidi and Palorinya; developed "
        "operational policies, aligned conduct standards with UNHCR standards, and "
        "supported office establishment and compliance.",
    )
    append_experience_details(
        "Regional MHPSS Technical Consultant",
        "The MHPSS Collaborative",
        "The CV describes this regional consultancy as continuing through January "
        "2023; the existing website record lists June 2022 only. Co-led development "
        "of a global MHPSS learning course involving experts from the Global North "
        "and South; assessed 60 humanitarian frontline workers in Uganda and "
        "Zimbabwe; and translated findings into curriculum development, supervision "
        "planning and a pilot learning report.",
    )
    append_experience_details(
        "Lead Peace Project Policy Analyst",
        "Mensen met een Missie",
        "The CV describes baseline policy analysis for the “Contributing to Peaceful "
        "and Safe Societies” programme across the Democratic Republic of the Congo, "
        "Burundi, Uganda and South Sudan. No additional dates are supplied in the CV.",
    )
    append_experience_details(
        "Chairperson of the Board (volunteer)",
        "Institute for Community-Based Sociotherapy",
        "The CV identifies this governance role as Board Chair, Institute for "
        "Community Based Sociotherapy (ICBS). No additional dates are supplied in "
        "the CV; the existing website dates and organization-name note are retained.",
    )
    append_experience_details(
        "Humanitarian Peer Supporter",
        "CoCreate Humanity",
        "The CV identifies this contribution as peer support membership. The existing "
        "website note records differing start descriptions from CoCreate Humanity "
        "and the profile chronology; those details remain unresolved.",
    )

    add_experience(
        "Fundraising and Grant Assistant",
        "Greater Upper Nile Peace Initiative",
        start_year=2015,
        start_month=8,
        end_year=2015,
        end_month=10,
        experience_type="employment",
        description="Conducted funding prospect research, mapped donors and philanthropic organisations, and supported fundraising strategy and proposal development.",
        sort_order=30,
    )
    add_experience(
        "Sexual and Gender-Based Violence Officer",
        "Inter-Aid",
        start_year=2015,
        start_month=4,
        end_year=2015,
        end_month=7,
        location="Kiryandongo Refugee Settlement, Uganda",
        experience_type="employment",
        description="Supported gender-based violence prevention and response, survivor-centred referral pathways and caseworker supervision; coordinated with UNHCR, partners and community structures; and prepared periodic reports.",
        sort_order=31,
    )
    add_experience(
        "Expert team member — conflict impact assessment",
        "Deutsche Gesellschaft für Internationale Zusammenarbeit (GIZ)",
        start_year=2024,
        end_year=2024,
        location="Great Lakes Region",
        experience_type="consultancy",
        description="Assessed the impact of conflict on MHPSS and peacebuilding in the Great Lakes Region.",
        sort_order=32,
    )
    add_experience(
        "Lead consultant and designer — SAFER HEELs",
        "ACT Church of Sweden / Sida",
        start_year=2024,
        end_year=2024,
        location="Uganda",
        experience_type="consultancy",
        description="Led consulting and design for a consortium project planned for 2025–2027 addressing psychosocial wellbeing, gender-based violence, sexual and reproductive health and rights, and peacebuilding in Uganda’s refugee settlements.",
        sort_order=33,
    )
    add_experience(
        "Youth Talk programme evaluation",
        "Search for Common Ground",
        start_year=2023,
        end_year=2023,
        location="Central African Republic",
        experience_type="consultancy",
        description="Evaluated the Youth Talk programme, focusing on adolescent MHPSS and transformative peacebuilding. This is a separate CV-described evaluation from the existing Youth Talk consultancy entry.",
        sort_order=34,
    )
    add_experience(
        "Visiting researcher and field coordinator",
        "Radboud University",
        start_year=2022,
        end_year=2023,
        experience_type="consultancy",
        description="Worked on a study of MHPSS and unintended social consequences.",
        sort_order=35,
    )
    add_experience(
        "Consultant / co-lead — MHPSS in protection and livelihoods",
        "Global Alliance for Africa",
        start_year=2021,
        end_year=2021,
        location="Kibera, Kenya",
        experience_type="consultancy",
        description="Co-led work integrating MHPSS into protection and livelihoods programming for LGBTQI+ communities. This is separate from the existing 2016 consultancy record.",
        sort_order=36,
    )

    resource_updates = {
        "unhcr-suicide-prevention-toolkit": {
            "published_year": 2022,
            "author_credit": "Obermeyer, M., Mukasa, M.B. and Ventevogel, P.",
            "publisher": "United Nations High Commissioner for Refugees",
        },
        "culture-context-mental-health-south-sudan-displacement": {
            "author_credit": "Tankink, M. et al., including Mukasa, M.B.",
            "publisher": "United Nations High Commissioner for Refugees",
        },
        "integrating-mhpss-peacebuilding-programs-practical-guide": {
            "author_credit": "Mukasa Bwesige, M. and contributors",
            "publisher": "Search for Common Ground",
        },
    }
    for slug, additions in resource_updates.items():
        resource = Resource.objects.using(database).filter(slug=slug).first()
        if not resource:
            continue
        changed_fields = []
        for field, value in additions.items():
            if not getattr(resource, field):
                setattr(resource, field, value)
                changed_fields.append(field)
        if slug == "unhcr-suicide-prevention-toolkit" and (
            "CV-supplied bibliographic details:" not in resource.description
        ):
            supplement = (
                "CV-supplied bibliographic details: "
                "Obermeyer, M., Mukasa, M.B. and Ventevogel, P.; UNHCR, 2022. "
                "The CV identifies Mukasa as a co-author. Existing source notes "
                "about unverified title-page credits are retained for review."
            )
            resource.description = (
                f"{resource.description}\n\n" if resource.description else ""
            ) + supplement
            changed_fields.append("description")
        if slug == "culture-context-mental-health-south-sudan-displacement" and (
            "CV-supplied contribution:" not in resource.description
        ):
            resource.description = (
                f"{resource.description}\n\n" if resource.description else ""
            ) + (
                "CV-supplied contribution: Tankink, M. et al., including Mukasa, "
                "M.B. The work is presented as an institutional UNHCR resource, "
                "not as a sole-authored publication."
            )
            changed_fields.append("description")
        if slug == "integrating-mhpss-peacebuilding-programs-practical-guide" and (
            "CV-supplied attribution:" not in resource.description
        ):
            resource.description = (
                f"{resource.description}\n\n" if resource.description else ""
            ) + (
                "CV-supplied attribution: Mukasa Bwesige, M. and contributors; "
                "Search for Common Ground."
            )
            changed_fields.append("description")
        if changed_fields:
            resource.save(using=database, update_fields=tuple(set(changed_fields)))


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0014_add_supplementary_professional_information"),
    ]

    operations = [
        migrations.RunPython(add_cv_profile_details, migrations.RunPython.noop),
    ]
