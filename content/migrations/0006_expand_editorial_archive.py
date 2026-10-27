import datetime

from django.db import migrations


def expand_editorial_archive(apps, schema_editor):
    database = schema_editor.connection.alias
    Profile = apps.get_model("content", "Profile")
    WorkArea = apps.get_model("content", "WorkArea")
    Resource = apps.get_model("content", "Resource")
    MediaAppearance = apps.get_model("content", "MediaAppearance")
    Insight = apps.get_model("content", "Insight")
    Organization = apps.get_model("content", "Organization")
    SourceReference = apps.get_model("content", "SourceReference")

    def source(title, url, publisher, status, notes):
        reference, _ = SourceReference.objects.using(database).get_or_create(
            url=url,
            defaults={
                "title": title,
                "publisher": publisher,
                "verification_status": status,
                "notes": notes,
            },
        )
        if reference.verification_status != status or reference.notes != notes:
            reference.verification_status = status
            reference.notes = notes
            reference.save(using=database)
        return reference

    refs = {
        "who": SourceReference.objects.using(database).get(
            url="https://www.who.int/news-room/feature-stories/detail/a-critical-step-toward-saving-lives--helping-humanitarian-workers-respond-to-substance-use-with-empathy-and-care"
        ),
        "cambridge": SourceReference.objects.using(database).get(
            url="https://www.cambridge.org/core/journals/global-mental-health/article/coping-mechanisms-adopted-following-a-suicide-attempt-among-refugees-in-humanitarian-settings-within-northern-uganda/2C8B3C0466F15977E75BF57F9F916BB3"
        ),
        "palorinya": SourceReference.objects.using(database).get(
            url="https://journals.lww.com/invn/fulltext/2021/19020/despair_and_suicide_related_behaviours_in.9.aspx"
        ),
        "cocreate": SourceReference.objects.using(database).get(
            url="https://www.cocreatehumanity.org/post/webinar-let-s-talk-life-understanding-suicide-and-promoting-mental-wellness-on-thursday-29-febru"
        ),
        "arq_interview": SourceReference.objects.using(database).get(
            url="https://arq.org/en/case/prioritising-mental-health-conflict-zones"
        ),
        "arq_reflection": SourceReference.objects.using(database).get(
            url="https://arq.org/en/case/co-creating-mhpss-knowledge-and-practice"
        ),
        "reliefweb": SourceReference.objects.using(database).get(
            url="https://reliefweb.int/report/world/providing-access-psychosocial-support-forcibly-displaced-persons-qa-moses-mukasa"
        ),
        "jrs_usa": source(
            "JRS Insider: Moses Mukasa on Centering Mental Health in Refugee Response",
            "https://www.jrsusa.org/story/jrs-insider-moses-mukasa-on-centering-mental-health-in-refugee-response/",
            "Jesuit Refugee Service USA",
            "confirmed",
            "Publisher page retrieved. It describes Mukasa's background in community-based mental health and humanitarian work and identifies his JRS role at publication.",
        ),
        "kigali": source(
            "Akarere k’Ibiyaga Bigari kahagurukiye gukemura ikibazo cy’ubuzima bwo mu mutwe",
            "https://www.kigalitoday.com/ubuzima/ubuvuzi/article/akarere-k-ibiyaga-bigari-kahagurukiye-gukemura-ikibazo-cy-ubuzima-bwo-mu-mutwe",
            "Kigali Today",
            "confirmed",
            "Publisher page retrieved in Kinyarwanda; dated 5 February 2025 and identifies Mukasa as a trainer with attributed comments.",
        ),
        "institute": source(
            "Great Lakes Research Institute for Mental Health & Wellbeing",
            "https://www.greatlakesresearchinstitute.org/",
            "Great Lakes Research Institute for Mental Health & Wellbeing",
            "confirmed",
            "Official site identifies the institute as established in 2025 and founded by Moses Bwesige Mukasa.",
        ),
        "critical_dialogues": SourceReference.objects.using(database).get(
            url="https://app.mhpss.net/criticaldialogues"
        ),
        "arq_news": SourceReference.objects.using(database).get(
            url="https://arq.org/en/news/towards-equitable-collaboration-mhpss"
        ),
        "undp": SourceReference.objects.using(database).get(
            url="https://www.undp.org/sites/g/files/zskgke326/files/2022-05/UNDP-Integrating-Mental-Health-and-Psychosocial-Support-into-Peacebuilding-V2.pdf"
        ),
    }

    profile = Profile.objects.using(database).filter(full_name="Mukasa Moses Bwesige").first()
    if profile:
        profile.short_biography = (
            "Mukasa Moses Bwesige works across mental health and psychosocial support "
            "(MHPSS), humanitarian response and suicide-related research. Published "
            "research examines suicide-related behaviour in Palorinya Refugee "
            "Settlement and coping after a suicide attempt among refugees in northern "
            "Uganda. His public record also includes interviews, training and "
            "reflection on community-led and context-sensitive support."
        )
        profile.biography = (
            "Mukasa Moses Bwesige is a Ugandan mental health and psychosocial support "
            "practitioner whose documented work connects humanitarian response, "
            "forced displacement, suicide prevention and community-based support. "
            "The JRS USA profile recounts his early interest in mental health during "
            "undergraduate study in psychology and social science, followed by "
            "volunteer experience at Uganda’s national mental health hospital and "
            "humanitarian protection work in South Sudan and the Democratic Republic "
            "of the Congo.\n\n"
            "His research record includes a 2021 paper on suicide-related behaviours "
            "in Palorinya Refugee Settlement and a 2026 Cambridge Prisms article on "
            "coping mechanisms following suicide attempts among refugees in northern "
            "Uganda. These are distinct publications with separate author lists and "
            "bibliographic records in the research library.\n\n"
            "Public interviews and institutional features document work and ideas "
            "around community-based MHPSS, suicide prevention, culturally grounded "
            "support, substance use in humanitarian settings, and the relationship "
            "between mental health and peacebuilding. Publisher-specific spellings "
            "are preserved in citations; the site uses Mukasa Moses Bwesige as its "
            "display name.\n\n"
            "Professional role descriptions are time-bound. WHO and JRS USA sources "
            "published in 2025 use different descriptions of his JRS remit; neither "
            "is presented here as confirmation of a current appointment. The "
            "Institute’s own website identifies Moses Bwesige Mukasa as its founder "
            "and gives 2025 as its founding year."
        )
        profile.experience = (
            "JRS USA’s 2025 profile describes a path from volunteer experience at "
            "Uganda’s national mental health hospital to humanitarian protection "
            "work in South Sudan and the Democratic Republic of the Congo, followed "
            "by a focus on community-based mental health and psychosocial support. "
            "A World Health Organization feature published on 8 October 2025 "
            "identified Mukasa as an Inter-Regional MHPSS officer at Jesuit Refugee "
            "Service in Uganda. JRS USA’s 2025 profile describes an interregional "
            "MHPSS role for East and South Africa. These are source-dated descriptions, "
            "not a claim about his current position."
        )
        profile.affiliations = (
            "The Great Lakes Research Institute for Mental Health & Wellbeing’s "
            "official website identifies Moses Bwesige Mukasa as its founder and "
            "the institute as established in 2025. JRS roles are described in "
            "time-specific 2025 publisher records; see the linked sources below."
        )
        profile.qualifications = (
            "A CoCreate Humanity speaker profile published in 2024 described "
            "doctoral research at Ghent University and graduate-level doctoral "
            "study at Makerere University. This is a dated description of research "
            "status, not evidence of a completed doctorate; no doctoral title or "
            "completed qualification is claimed on this site."
        )
        profile.save(using=database)
        profile.source_references.add(
            refs["who"],
            refs["jrs_usa"],
            refs["cocreate"],
            refs["institute"],
            refs["cambridge"],
            refs["palorinya"],
        )

    organization_data = [
        {
            "slug": "jesuit-refugee-service",
            "title": "Jesuit Refugee Service",
            "summary": "Humanitarian organisation described in publisher records documenting Mukasa’s MHPSS work in 2025.",
            "description": (
                "WHO and Jesuit Refugee Service USA publisher pages in 2025 described "
                "Mukasa in interregional mental health and psychosocial support roles. "
                "Those descriptions are retained as historical source context, not "
                "as confirmation of a current appointment."
            ),
            "source_url": refs["who"].url,
            "website_url": "https://www.jrs.net/",
            "source_attribution": "World Health Organization; Jesuit Refugee Service USA",
            "is_published": True,
            "order": 1,
        },
        {
            "slug": "great-lakes-research-institute",
            "title": "Great Lakes Research Institute for Mental Health & Wellbeing",
            "summary": "A Kampala-based research and knowledge institution founded in 2025, according to its official website.",
            "description": (
                "The institute’s public site describes work in research, capacity "
                "building and public discussion, grounded in community knowledge "
                "from the Great Lakes region. Its own website identifies Moses "
                "Bwesige Mukasa as founder."
            ),
            "source_url": refs["institute"].url,
            "website_url": refs["institute"].url,
            "source_attribution": "Great Lakes Research Institute for Mental Health & Wellbeing",
            "is_published": True,
            "is_featured": True,
            "order": 2,
        },
    ]
    organizations = {}
    for values in organization_data:
        organization, _ = Organization.objects.using(database).update_or_create(
            slug=values["slug"],
            defaults=values,
        )
        organizations[values["slug"]] = organization

    area_copy = {
        "mental-health-and-psychosocial-support": {
            "summary": "Humanitarian MHPSS, including substance-use response, community support and care shaped by context.",
            "description": (
                "Mental health and psychosocial support in emergencies involves "
                "more than clinical care: humanitarian workers, local services and "
                "communities all shape whether people can access timely, respectful "
                "support. The World Health Organization’s 2025 feature on responding "
                "to substance use in humanitarian settings quotes Mukasa on the "
                "importance of equipping responders to recognise and respond to "
                "substance-related conditions.\n\n"
                "The same feature describes orientation materials developed for "
                "humanitarian workers and field-tested between 2024 and 2025. It is "
                "a WHO-authored feature, not a publication authored by Mukasa. "
                "Related interviews and research are linked below."
            ),
            "source_url": refs["who"].url,
            "source_attribution": "World Health Organization (publisher feature, 2025)",
        },
        "suicide-prevention-and-research": {
            "summary": "Peer-reviewed research and public training on suicide-related behaviour and coping in refugee settings.",
            "description": (
                "The documented research spans suicide-related behaviour in "
                "Palorinya Refugee Settlement and coping mechanisms following a "
                "suicide attempt among refugees in northern Uganda. The later "
                "Cambridge Prisms article describes a mixed-method study of "
                "South Sudanese refugees across four northern Ugandan settlements; "
                "its publisher presents the work as relevant to MHPSS programming.\n\n"
                "Public training records add a practice-facing strand: a CoCreate "
                "Humanity webinar on suicide and mental wellness and English- and "
                "Ukrainian-language training recordings catalogued through ARQ "
                "International. Individual recordings are linked to their sources; "
                "unconfirmed video titles and dates are not supplied."
            ),
            "source_url": refs["cambridge"].url,
            "source_attribution": "Cambridge Prisms: Global Mental Health; Intervention",
        },
        "humanitarian-and-refugee-mental-health": {
            "summary": "Research and public accounts of MHPSS in forced displacement and humanitarian response.",
            "description": (
                "Forced displacement is a recurring context across the documented "
                "research and public record. The Palorinya paper concerns "
                "refugees in a settlement in northern Uganda; the Cambridge study "
                "examines coping after suicide attempts among refugees in the "
                "region. A Jesuit Refugee Service Q&A and a JRS USA profile provide "
                "institutional accounts of psychosocial support and humanitarian "
                "work. The archive identifies each item’s publisher and does not "
                "treat an interview or feature as a research paper."
            ),
            "source_url": refs["reliefweb"].url,
            "source_attribution": "Jesuit Refugee Service / ReliefWeb; JRS USA",
        },
        "community-led-and-culturally-grounded-support": {
            "summary": "Community knowledge, locally grounded support and the role of affected people in shaping MHPSS.",
            "description": (
                "Community-led practice treats local knowledge and relationships "
                "as central to how support is understood and delivered. A JRS USA "
                "profile describes Mukasa’s work with community-based initiatives "
                "and recounts how local helpers were supported in displacement "
                "settings. An ARQ-published reflection addresses co-creating MHPSS "
                "knowledge and practice; the publisher’s byline uses the spelling "
                "“Mukasa Moses Wasige.”\n\n"
                "These sources document themes and attributed work; they are not "
                "evidence that one approach applies uniformly across communities."
            ),
            "source_url": refs["arq_reflection"].url,
            "source_attribution": "ARQ International; Jesuit Refugee Service USA",
        },
        "mental-health-conflict-and-peacebuilding": {
            "summary": "Public discussion and training coverage connecting MHPSS with conflict, displacement and peacebuilding.",
            "description": (
                "An ARQ interview discusses mental health in conflict zones and "
                "the risks of interventions that are not adequately grounded in "
                "context. Separately, Kigali Today’s Kinyarwanda-language report "
                "covers an ICGLR and Rwanda MINAFFET training in Kigali in February "
                "2025 and quotes Mukasa in his capacity as a trainer. The coverage "
                "connects psychosocial healing with peacebuilding; it is a news "
                "report, not an authored research output.\n\n"
                "The ICGLR-RTF training report is linked as an institutional "
                "resource, with its own publisher attribution."
            ),
            "source_url": refs["kigali"].url,
            "source_attribution": "Kigali Today; ARQ International",
        },
        "equitable-collaboration-and-localisation": {
            "summary": "Reflection on co-creating MHPSS knowledge through humility, respect and more equitable collaboration.",
            "description": (
                "The ARQ reflection “Co-Creating MHPSS Knowledge and Practice” "
                "addresses collaboration, humility, respect and the decolonisation "
                "of MHPSS research and practice. It is a personal reflection "
                "published by ARQ, not a peer-reviewed research article; the "
                "publisher’s source-specific byline is preserved in the record.\n\n"
                "The related ARQ symposium material and a MHPSS Network dialogue "
                "are included in the media archive with dates and source notes. "
                "This theme describes the content of those sources rather than "
                "claiming an independently measured impact."
            ),
            "source_url": refs["arq_reflection"].url,
            "source_attribution": "ARQ International",
        },
    }
    areas = {}
    for slug, values in area_copy.items():
        area = WorkArea.objects.using(database).filter(slug=slug).first()
        if not area:
            continue
        for field, value in values.items():
            setattr(area, field, value)
        area.save(using=database)
        areas[slug] = area
        area.source_references.add(
            *{
                "mental-health-and-psychosocial-support": [refs["who"]],
                "suicide-prevention-and-research": [refs["cambridge"], refs["palorinya"], refs["cocreate"]],
                "humanitarian-and-refugee-mental-health": [refs["reliefweb"], refs["jrs_usa"]],
                "community-led-and-culturally-grounded-support": [refs["arq_reflection"], refs["jrs_usa"]],
                "mental-health-conflict-and-peacebuilding": [refs["arq_interview"], refs["kigali"]],
                "equitable-collaboration-and-localisation": [refs["arq_reflection"], refs["arq_news"]],
            }[slug]
        )

    resource_data = [
        {
            "slug": "despair-and-suicide-related-behaviours-palorinya",
            "journal_name": "Intervention",
            "volume": "19",
            "issue": "2",
            "page_range": "224–232",
            "description": (
                "This peer-reviewed field report examines despair and "
                "suicide-related behaviours among refugees in Palorinya Refugee "
                "Settlement, Moyo, Uganda. Its focus places suicide-related "
                "experience in the setting of forced displacement and the "
                "conditions of settlement life. The publisher page was not "
                "available during this source check; DOI and citation details "
                "are recorded from the supplied research dossier."
            ),
            "source_attribution": "Intervention, 19(2), 224–232 (2021)",
        },
        {
            "slug": "coping-mechanisms-after-a-suicide-attempt",
            "journal_name": "Cambridge Prisms: Global Mental Health",
            "volume": "13",
            "issue": "",
            "page_range": "",
            "summary": (
                "A mixed-method study of coping mechanisms following suicide "
                "attempts among South Sudanese refugees in four settlements in "
                "northern Uganda."
            ),
            "description": (
                "The publisher describes a concurrent mixed-method study of "
                "coping following suicide attempts among adult South Sudanese "
                "refugees in four settlements in northern Uganda. The article "
                "examines how people understand and respond to the aftermath of "
                "an attempt, with the authors discussing relevance to humanitarian "
                "MHPSS programming. This summary is based on the publisher’s "
                "article page and is not a substitute for the full paper."
            ),
            "source_attribution": "Cambridge Prisms: Global Mental Health, Volume 13 (2026)",
        },
    ]
    for values in resource_data:
        resource = Resource.objects.using(database).get(slug=values["slug"])
        for field, value in values.items():
            setattr(resource, field, value)
        resource.save(using=database)

    who = Resource.objects.using(database).get(slug="who-substance-use-empathy-humanitarian-workers")
    who.resource_type = "feature"
    who.description = (
        "This World Health Organization feature explains why people affected by "
        "substance use can be overlooked in humanitarian response. It quotes "
        "Mukasa Moses Bwesige, identified in the article as an Inter-Regional "
        "MHPSS officer at Jesuit Refugee Service in Uganda at publication. WHO "
        "reports that orientation materials were field-tested with frontline "
        "workers in eight crisis-affected locations during 2024–2025. The item "
        "is authored by WHO; Mukasa is a quoted contributor, not the article’s author."
    )
    who.author_credit = "World Health Organization; includes an attributed statement from Mukasa Moses Bwesige."
    who.save(using=database)
    refs["who"].resources.add(who)
    who.organizations.add(
        Organization.objects.using(database).get(slug="jesuit-refugee-service")
    )

    kigali, _ = Resource.objects.using(database).get_or_create(
        slug="kigali-today-mental-health-peacebuilding-training",
        defaults={
            "title": "Akarere k’Ibiyaga Bigari kahagurukiye gukemura ikibazo cy’ubuzima bwo mu mutwe",
            "summary": (
                "Kinyarwanda-language reporting on an ICGLR and Rwanda MINAFFET "
                "training about mental health and peacebuilding; Mukasa is "
                "identified as a trainer and quoted."
            ),
            "description": (
                "Kigali Today’s report covers a four-day regional training in "
                "Kigali beginning 4 February 2025. The article identifies Mukasa "
                "as a trainer and reports his comments on the continuing effects "
                "of conflict and the importance of psychosocial healing. The "
                "original article is in Kinyarwanda; this English description "
                "summarises the report and does not represent it as his authored work."
            ),
            "resource_type": "feature",
            "author_credit": "Simon Kamuzinzi, Kigali Today",
            "source_attribution": "Kigali Today (Kinyarwanda)",
            "source_url": refs["kigali"].url,
            "published_on": datetime.date(2025, 2, 5),
            "published_year": 2025,
            "is_published": True,
            "is_featured": True,
            "order": 4,
        },
    )
    kigali.resource_type = "feature"
    kigali.author_credit = "Simon Kamuzinzi, Kigali Today"
    kigali.source_attribution = "Kigali Today (Kinyarwanda)"
    kigali.published_on = datetime.date(2025, 2, 5)
    kigali.published_year = 2025
    kigali.is_published = True
    kigali.is_featured = True
    kigali.source_references.add(refs["kigali"])

    institute_resource, _ = Resource.objects.using(database).get_or_create(
        slug="great-lakes-research-institute",
        defaults={
            "title": "Great Lakes Research Institute for Mental Health & Wellbeing",
            "summary": (
                "The institute’s official website describes its research, "
                "capacity-building and public knowledge work in the Great Lakes region."
            ),
            "description": (
                "The institute’s public site identifies Moses Bwesige Mukasa as "
                "its founder and gives 2025 as its founding year. This is an "
                "institutional resource, not an authored publication or an "
                "independent evaluation of its work."
            ),
            "resource_type": "other",
            "author_credit": "Great Lakes Research Institute for Mental Health & Wellbeing",
            "source_attribution": "Official institute website",
            "source_url": refs["institute"].url,
            "published_year": 2025,
            "is_published": True,
            "is_featured": True,
            "order": 5,
        },
    )
    institute_resource.source_references.add(refs["institute"])

    unconfirmed_institutional = Resource.objects.using(database).filter(
        slug="undp-integrating-mhpss-into-peacebuilding"
    ).first()
    if unconfirmed_institutional:
        unconfirmed_institutional.summary = (
            "UNDP institutional report on integrating MHPSS into peacebuilding. "
            "Included as contextual reading only; no individual authorship or "
            "contribution is attributed here. Direct PDF retrieval was unavailable "
            "during this source check."
        )
        unconfirmed_institutional.is_published = False
        unconfirmed_institutional.save(using=database)

    appearance_updates = {
        "lets-talk-life-understanding-suicide-mental-wellness": (
            "The CoCreate Humanity announcement identifies Mukasa as the expert "
            "speaker and outlines a session on suicide terminology, drivers and "
            "explanatory models, followed by coping, resilience and mental wellness. "
            "The event took place on 29 February 2024. The publisher says the first "
            "hour was recorded and the interactive Q&A was not.",
            datetime.date(2024, 2, 29),
        ),
        "suicide-prevention-training-english": (
            "English-language recording of an ARQ International suicide-prevention "
            "training session for MHPSS practitioners in Ukraine. The source "
            "announcement identifies Mukasa as trainer and describes the programme "
            "as involving WHO Ukraine and the national MHPSS Technical Working "
            "Group. Exact session date, duration, transcript and on-platform title "
            "were not established.",
            None,
        ),
        "suicide-prevention-training-ukrainian": (
            "Ukrainian-language recording of the ARQ International suicide-prevention "
            "training for MHPSS practitioners in Ukraine. The source announcement "
            "identifies Mukasa as trainer. Exact session date, duration, transcript "
            "and on-platform title were not established.",
            None,
        ),
        "prioritising-mental-health-in-conflict-zones": (
            "ARQ International’s interview discusses mental health and psychosocial "
            "support in conflict and displacement settings, personal motivation, "
            "and caution about interventions that may cause harm. ARQ’s retrospective "
            "account also identifies Mukasa as one of four panellists at its 2023 "
            "conference marking 50 years of psychotrauma knowledge-sharing.",
            None,
        ),
        "providing-access-to-psychosocial-support-forcibly-displaced-persons": (
            "A Jesuit Refugee Service Q&A about access to psychosocial support for "
            "forcibly displaced people. The publisher page could not be retrieved "
            "during this check, so the archive preserves the source title and link "
            "without adding an unverified date or interview detail.",
            None,
        ),
        "jrs-insider-centering-mental-health": (
            "JRS USA’s profile recounts Mukasa’s path into humanitarian work and "
            "describes community-based and community-led support for displaced "
            "people. It is an institutional profile, not a research paper. The "
            "publisher page was checked; only the year is displayed because an "
            "exact publication day was not confirmed.",
            None,
        ),
        "mhpss-network-critical-dialogues": (
            "The MHPSS Network entry describes the first Critical Dialogues plenary "
            "on power, politics and practice in MHPSS and lists Mukasa among the "
            "panel participants. The source page was access-restricted during this "
            "check; date and description follow the research source register.",
            datetime.date(2025, 7, 3),
        ),
        "towards-equitable-collaboration-in-mhpss": (
            "ARQ International’s 2025 symposium coverage and video compilation "
            "include a reflection on co-creating MHPSS knowledge and practice. "
            "The related personal reflection is separately listed in Insights "
            "under the publisher’s source-specific byline.",
            datetime.date(2025, 11, 3),
        ),
    }
    for slug, (description, published_on) in appearance_updates.items():
        appearance = MediaAppearance.objects.using(database).filter(slug=slug).first()
        if not appearance:
            continue
        appearance.description = description
        if published_on:
            appearance.published_on = published_on
            appearance.published_year = published_on.year
        if slug in {
            "mhpss-network-critical-dialogues",
            "towards-equitable-collaboration-in-mhpss",
        }:
            appearance.is_published = True
        appearance.save(using=database)

    new_appearances = [
        {
            "slug": "kigali-today-mental-health-peacebuilding-training",
            "title": "Regional training on mental health and peacebuilding in Kigali",
            "summary": (
                "Kigali Today’s report identifies Mukasa as a trainer and quotes "
                "him on psychosocial healing after conflict."
            ),
            "description": (
                "The Kinyarwanda-language news report covers an ICGLR and Rwanda "
                "MINAFFET training in Kigali beginning 4 February 2025. Mukasa is "
                "identified as a trainer and quoted on the lasting effects of "
                "conflict and the role of psychosocial healing. The original "
                "publisher’s article is linked; this archive entry is not an "
                "authored article."
            ),
            "media_type": "feature",
            "language": "other",
            "published_on": datetime.date(2025, 2, 5),
            "published_year": 2025,
            "source": "Kigali Today",
            "source_url": refs["kigali"].url,
            "original_url": refs["kigali"].url,
            "is_published": True,
            "is_featured": True,
            "order": 4,
        },
        {
            "slug": "arq-psychotrauma-conference-panel",
            "title": "ARQ International conference on psychotrauma knowledge-sharing",
            "summary": (
                "ARQ’s later interview identifies Mukasa as one of four panellists "
                "at its 2023 conference."
            ),
            "description": (
                "ARQ International’s interview page retrospectively identifies "
                "Mukasa as one of four panellists at a 2023 conference marking "
                "50 years of psychotrauma knowledge-sharing. The linked record "
                "is ARQ’s interview; no separate event recording is claimed."
            ),
            "media_type": "conference",
            "language": "en",
            "published_year": 2023,
            "source": "ARQ International",
            "source_url": refs["arq_interview"].url,
            "original_url": refs["arq_interview"].url,
            "is_published": True,
            "order": 5,
        },
    ]
    for values in new_appearances:
        appearance, _ = MediaAppearance.objects.using(database).get_or_create(
            slug=values["slug"],
            defaults=values,
        )
        appearance.source_references.add(
            refs["kigali"] if appearance.slug.startswith("kigali-") else refs["arq_interview"]
        )
    MediaAppearance.objects.using(database).filter(
        slug="jrs-insider-centering-mental-health"
    ).first().organizations.add(
        Organization.objects.using(database).get(slug="jesuit-refugee-service")
    )

    reflection = Insight.objects.using(database).filter(
        slug="co-creating-mhpss-knowledge-and-practice"
    ).first()
    if reflection:
        reflection.published_on = datetime.date(2025, 12, 3)
        reflection.published_year = 2025
        reflection.original_source = "ARQ International"
        reflection.summary = (
            "An ARQ-published personal reflection on co-creating MHPSS knowledge "
            "and practice through collaboration, humility and respect."
        )
        reflection.description = (
            "ARQ’s reflection page attributes this piece to “Mukasa Moses Wasige”; "
            "that source-specific spelling is retained here as the publisher’s "
            "byline. The reflection considers co-creation, humility, respect and "
            "decolonising MHPSS research and practice. It is presented as a personal "
            "reflection, not as a peer-reviewed article."
        )
        reflection.save(using=database)
        reflection.source_references.add(refs["arq_reflection"])

    area_by_slug = areas
    resource_topics = {
        "despair-and-suicide-related-behaviours-palorinya": [
            "suicide-prevention-and-research",
            "humanitarian-and-refugee-mental-health",
        ],
        "coping-mechanisms-after-a-suicide-attempt": [
            "suicide-prevention-and-research",
            "humanitarian-and-refugee-mental-health",
        ],
        "who-substance-use-empathy-humanitarian-workers": [
            "mental-health-and-psychosocial-support",
            "humanitarian-and-refugee-mental-health",
        ],
        "kigali-today-mental-health-peacebuilding-training": [
            "mental-health-conflict-and-peacebuilding",
            "mental-health-and-psychosocial-support",
        ],
        "great-lakes-research-institute": [
            "community-led-and-culturally-grounded-support",
            "equitable-collaboration-and-localisation",
        ],
    }
    for slug, topic_slugs in resource_topics.items():
        resource = Resource.objects.using(database).filter(slug=slug).first()
        if resource:
            resource.related_areas.add(
                *(area_by_slug[topic] for topic in topic_slugs if topic in area_by_slug)
            )

    media_topics = {
        "lets-talk-life-understanding-suicide-mental-wellness": [
            "suicide-prevention-and-research",
        ],
        "suicide-prevention-training-english": ["suicide-prevention-and-research"],
        "suicide-prevention-training-ukrainian": ["suicide-prevention-and-research"],
        "prioritising-mental-health-in-conflict-zones": [
            "mental-health-conflict-and-peacebuilding",
            "humanitarian-and-refugee-mental-health",
        ],
        "providing-access-to-psychosocial-support-forcibly-displaced-persons": [
            "humanitarian-and-refugee-mental-health",
        ],
        "jrs-insider-centering-mental-health": [
            "community-led-and-culturally-grounded-support",
            "humanitarian-and-refugee-mental-health",
        ],
        "mhpss-network-critical-dialogues": [
            "equitable-collaboration-and-localisation",
        ],
        "towards-equitable-collaboration-in-mhpss": [
            "equitable-collaboration-and-localisation",
        ],
        "kigali-today-mental-health-peacebuilding-training": [
            "mental-health-conflict-and-peacebuilding",
        ],
        "arq-psychotrauma-conference-panel": [
            "mental-health-conflict-and-peacebuilding",
        ],
    }
    for slug, topic_slugs in media_topics.items():
        appearance = MediaAppearance.objects.using(database).filter(slug=slug).first()
        if appearance:
            appearance.related_areas.add(
                *(area_by_slug[topic] for topic in topic_slugs if topic in area_by_slug)
            )

    if reflection and "equitable-collaboration-and-localisation" in area_by_slug:
        reflection.related_areas.add(area_by_slug["equitable-collaboration-and-localisation"])


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0005_alter_mediaappearance_media_type"),
    ]

    operations = [
        migrations.RunPython(expand_editorial_archive, migrations.RunPython.noop),
    ]
