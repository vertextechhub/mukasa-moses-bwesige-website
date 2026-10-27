from datetime import date
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.staticfiles import finders
from django.test import Client, TestCase
from django.test.utils import override_settings
from django.urls import reverse
from django.templatetags.static import static

from .forms import ContactForm
from .models import (
    ContactMessage,
    Insight,
    MediaAppearance,
    ProfessionalExperience,
    Resource,
    WorkArea,
)


class PageTests(TestCase):
    def test_required_pages_are_available(self):
        for name in ("home", "about", "areas", "media", "publications", "insights", "contact"):
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_supplied_images_render_on_relevant_pages(self):
        images_by_page = {
            "home": ("images (3).jfif",),
            "about": ("images (4).jfif",),
            "areas": ("images (1).jfif",),
            "media": (
                "images (2).jfif",
                "images.jfif",
                "images (5).jfif",
                "WhatsApp Image 2026-10-26 at 17.44.16.jpeg",
                "WhatsApp Image 2026-10-26 at 17.44.17.jpeg",
                "WhatsApp Image 2026-10-26 at 17.44.18.jpeg",
            ),
            "publications": ("Interior_No_Cover_page-0001 (1).jpg",),
        }

        for page, filenames in images_by_page.items():
            with self.subTest(page=page):
                response = self.client.get(reverse(page))
                self.assertEqual(response.status_code, 200)
                for filename in filenames:
                    with self.subTest(filename=filename):
                        image_path = f"images/{filename}"
                        self.assertTrue(finders.find(image_path), image_path)
                        image_url = static(image_path)
                        self.assertTrue(image_url.startswith("/static/"), image_url)
                        self.assertContains(response, f'src="{image_url}"')

    def test_home_uses_verified_name_without_invented_profile(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Moses Bwesige Mukasa")
        self.assertContains(response, "Rethinking mental health.")
        self.assertContains(response, "More than a decade of professional experience")
        self.assertContains(response, "Data Processing Officer")
        self.assertContains(response, "Full chronology")
        self.assertContains(response, "Explore my work")
        self.assertContains(response, reverse("areas"))
        self.assertContains(response, reverse("publications"))
        self.assertContains(response, "Global Mission-Oriented Transformation Protection Technical Specialist")
        self.assertContains(response, "Global Mission Transformation – Protection Specialist")
        self.assertContains(response, "Global Virtual Office, Global Mission Transformation Unit")
        self.assertContains(response, "Joint PhD candidate")
        self.assertNotContains(response, "Dr. Moses")
        self.assertNotContains(response, "doctorate completed")

    def test_unpublished_content_is_not_visible(self):
        WorkArea.objects.create(title="Private draft", is_published=False)
        Resource.objects.create(title="Unpublished paper", is_published=False)
        MediaAppearance.objects.create(title="Unpublished recording", is_published=False)
        for page, hidden in (
            ("areas", "Private draft"),
            ("publications", "Unpublished paper"),
            ("media", "Unpublished recording"),
        ):
            response = self.client.get(reverse(page))
            self.assertNotContains(response, hidden)

    def test_private_research_directory_is_not_served(self):
        for path in (
            "/private_research/",
            "/private_research/editorial_review.md",
            "/private_research/dr_website_research_source_register.md",
        ):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 404)

    def test_seeded_content_appears_with_attribution_and_original_links(self):
        publications = self.client.get(reverse("publications"))
        self.assertContains(publications, "Moses Mukasa, Roscoe Kasujja, Benjamin Alipanga")
        self.assertContains(publications, "10.1017/gmh.2026.10263")
        self.assertContains(publications, "not listed as the author")
        peacebuilding_resource = self.client.get(
            reverse("publications"),
            {"q": "Integrating Mental Health and Psychosocial Support into Peacebuilding"},
        )
        self.assertContains(peacebuilding_resource, "Integrating Mental Health and Psychosocial Support into Peacebuilding")
        self.assertContains(peacebuilding_resource, "No individual authorship or contribution by Mukasa is attributed")
        self.assertTrue(Resource.objects.filter(slug="unhcr-suicide-prevention-toolkit", is_published=True).exists())
        self.assertTrue(Resource.objects.filter(slug="undp-integrating-mhpss-into-peacebuilding", is_published=True).exists())
        self.assertEqual(
            Resource.objects.get(slug="unhcr-suicide-prevention-toolkit").author_credit,
            "Obermeyer, M., Mukasa, M.B. and Ventevogel, P.",
        )
        second_publication_page = self.client.get(reverse("publications"), {"page": "2"})
        self.assertContains(second_publication_page, "Planning for Prevention and Risk Mitigation")
        self.assertContains(second_publication_page, "Despair and Suicide-Related Behaviours in Palorinya")
        self.assertContains(second_publication_page, "Intervention")
        self.assertContains(second_publication_page, "title-page credits remain unverified")
        self.assertContains(second_publication_page, "Supplementary publication detail supplied: 2022.")
        self.assertContains(publications, "Kigali Today")
        self.assertContains(publications, "Kinyarwanda")

        media = self.client.get(reverse("media"))
        self.assertContains(
            media,
            "Let&#x27;s talk life - Understanding Suicide and Promoting Mental Wellness",
        )
        self.assertContains(media, "Webinar on Suicide prevention [09.04.2025, ENG]")
        self.assertContains(media, "Вебінар: «Запобігання самогубствам» [09.04.2025, UKR]")
        self.assertContains(media, "https://youtu.be/7MGL_-A3f2k")
        self.assertContains(media, "https://youtu.be/Ei3yxHCVP-g")
        self.assertContains(media, "MHPSS Network Critical Dialogues")
        self.assertContains(
            media,
            "This Much I Know: Practitioners Reflect on Community-Based MHPSS",
        )
        self.assertContains(
            media,
            "JRS Insider: Moses Mukasa on Centering Mental Health in Refugee Response",
        )
        self.assertContains(media, "Regional training on mental health and peacebuilding in Kigali")
        self.assertTrue(MediaAppearance.objects.filter(slug="mhpss-network-critical-dialogues", is_published=True).exists())
        self.assertTrue(MediaAppearance.objects.filter(slug="towards-equitable-collaboration-in-mhpss", is_published=True).exists())

    def test_video_archive_metadata_is_verified_and_source_pages_are_not_embedded(self):
        videos = {
            "lets-talk-life-understanding-suicide-mental-wellness": (
                "Let's talk life - Understanding Suicide and Promoting Mental "
                "Wellness with Mukasa Moses Bwesige",
                "https://youtu.be/FdSQr1MCsmo",
            ),
            "suicide-prevention-training-english": (
                "Webinar on Suicide prevention [09.04.2025, ENG]",
                "https://youtu.be/7MGL_-A3f2k",
            ),
            "suicide-prevention-training-ukrainian": (
                "Вебінар: «Запобігання самогубствам» [09.04.2025, UKR]",
                "https://youtu.be/Ei3yxHCVP-g",
            ),
        }
        for slug, (title, url) in videos.items():
            with self.subTest(slug=slug):
                item = MediaAppearance.objects.get(slug=slug, is_published=True)
                self.assertEqual(item.title, title)
                self.assertEqual(item.original_url, url)
                self.assertEqual(item.privacy_embed_url, url.replace("youtu.be", "www.youtube-nocookie.com/embed"))

        english = MediaAppearance.objects.get(slug="suicide-prevention-training-english")
        ukrainian = MediaAppearance.objects.get(slug="suicide-prevention-training-ukrainian")
        self.assertEqual(english.source, "MHPSS TWG Ukraine")
        self.assertEqual(english.published_year, 2025)
        self.assertEqual(english.language, MediaAppearance.Language.ENGLISH)
        self.assertEqual(ukrainian.source, "MHPSS TWG Ukraine")
        self.assertEqual(ukrainian.published_year, 2025)
        self.assertEqual(ukrainian.language, MediaAppearance.Language.UKRAINIAN)

        this_much_i_know = MediaAppearance.objects.get(
            slug="this-much-i-know-community-based-mhpss",
        )
        self.assertEqual(this_much_i_know.embed_url, "")
        self.assertEqual(this_much_i_know.media_type, MediaAppearance.MediaType.WEBINAR)
        jrs_feature = MediaAppearance.objects.get(slug="jrs-insider-centering-mental-health")
        self.assertEqual(jrs_feature.media_type, MediaAppearance.MediaType.FEATURE)
        self.assertEqual(jrs_feature.embed_url, "")

        response = self.client.get(reverse("media"), {"q": "Webinar on Suicide prevention"})
        self.assertContains(response, 'data-embed-url="https://www.youtube-nocookie.com/embed/7MGL_-A3f2k"')
        self.assertNotContains(response, "autoplay")
        source_only = self.client.get(
            reverse("media"),
            {"q": "This Much I Know"},
        )
        self.assertContains(source_only, "does not embed or label it as a recording")
        self.assertContains(source_only, "View original source page")
        self.assertNotContains(source_only, "<iframe")

        insights = self.client.get(reverse("insights"))
        self.assertContains(insights, "Co-Creating MHPSS Knowledge and Practice")
        self.assertContains(insights, "Mukasa Moses Wasige")
        self.assertContains(insights, "2025")
        self.assertNotContains(insights, "Suicidal Behaviour Beyond Individual Risk Profiles")

    def test_about_does_not_show_empty_editorial_warnings(self):
        response = self.client.get(reverse("about"))
        self.assertContains(response, "Moses Bwesige Mukasa")
        self.assertContains(response, "Global Mission-Oriented Transformation Protection Technical Specialist")
        self.assertContains(response, "joint PhD candidate")
        self.assertContains(response, "Jun 2026 – present")
        self.assertContains(response, reverse("areas"))
        self.assertContains(response, reverse("publications"))
        self.assertContains(response, reverse("media"))
        self.assertContains(response, "Professional experience")
        self.assertNotContains(response, "awaiting confirmation")
        self.assertContains(response, "Inter-Regional MHPSS Officer")
        self.assertContains(response, "Global Mission Transformation – Protection Specialist")
        self.assertContains(response, "doctoral researcher jointly affiliated")
        self.assertContains(response, "South Sudanese refugees")
        self.assertContains(response, "Reflexive Training: Reimagining Trainers of Trainers")
        self.assertContains(response, "master’s qualifications in Public Health and Counselling Psychology")
        self.assertContains(response, "PhD candidate — Clinical Psychology and Educational Sciences")
        self.assertContains(response, "Master of Public Health — Health Promotion")
        self.assertContains(response, "Bachelor of Arts — Social Sciences")
        self.assertContains(response, "Counselling Psychology is preserved pending confirmation")
        self.assertNotContains(response, "Dr. Moses")
        self.assertNotContains(response, "Selected public record")
        self.assertNotContains(response, "Profile sources")

    def test_professional_experience_is_chronological_sourced_and_preserves_conflicts(self):
        response = self.client.get(reverse("about"))
        page = response.content.decode()

        self.assertContains(response, "After undergraduate study; date not stated")
        self.assertContains(response, "Data Processing Officer")
        self.assertContains(response, "Uganda Bureau of Statistics")
        self.assertContains(response, "Inter-Regional MHPSS Officer")
        self.assertContains(response, "Lead Facilitator — MHPSS &amp; Peacebuilding Training of Trainers")
        self.assertContains(response, "Global Mission-Oriented Transformation Protection Technical Specialist")
        self.assertContains(response, "JRS start dates differ")
        self.assertContains(response, "roles overlap")
        self.assertContains(response, "Simbi Foundation page uses the name")
        self.assertContains(response, "LinkedIn source")
        self.assertContains(response, "https://www.linkedin.com/in/moses-bwesige-mukasa-6b2625183")
        self.assertLess(page.index("Data Processing Officer"), page.index("Assistant Project Officer"))
        self.assertLess(page.index("Assistant Project Officer"), page.index("Psychosocial Officer"))
        chronology = page.split('id="professional-experience"', 1)[1]
        self.assertLess(
            chronology.index("Inter-Regional MHPSS Officer"),
            chronology.index("Global Mission-Oriented"),
        )

        earliest_dated = ProfessionalExperience.objects.filter(
            is_published=True,
            start_year__isnull=False,
        ).order_by("start_year", "start_month", "sort_order").first()
        self.assertEqual(earliest_dated.start_year, 2014)
        self.assertEqual(ProfessionalExperience.objects.filter(is_published=True).count(), 28)

    def test_cv_supplements_preserve_and_flag_conflicting_career_information(self):
        response = self.client.get(reverse("about"))
        for value in (
            "Protection Technical Specialist, Global Mission-Oriented Transformation (GMT), June 2026–Present",
            "CV period: April 2023–Present",
            "The CV lists this role as current alongside the GMT appointment",
            "CV title and period: Country Programme MHPSS and Peacebuilding Technical Specialist",
            "CV title and period: Project Officer, Psychosocial, 2017–2019",
            "Fundraising and Grant Assistant",
            "Sexual and Gender-Based Violence Officer",
            "Expert team member — conflict impact assessment",
            "ACT Church of Sweden / Sida",
            "Radboud University",
            "IASC Reference Group on MHPSS and Peacebuilding",
            "Lewis &amp; Clark Graduate School of Education and Counseling",
            "Core Humanitarian Standards",
            "Angola, Burundi, Central African Republic",
            "English — fluent",
            "The CV separately describes regional technical leadership across 14 countries and lists 15 countries",
        ):
            with self.subTest(value=value):
                self.assertContains(response, value)

        jrs_history = ProfessionalExperience.objects.get(
            title="Inter-Regional MHPSS Officer — East & Southern Africa",
            organization="Jesuit Refugee Service (JRS)",
        )
        self.assertIn("CV period: April 2023–Present", jrs_history.description)
        self.assertIn("differs from the existing website record", jrs_history.description)
        self.assertTrue(
            ProfessionalExperience.objects.filter(
                title="Sexual and Gender-Based Violence Officer",
                organization="Inter-Aid",
                start_year=2015,
            ).exists()
        )

    def test_cv_publication_attributions_are_added_without_replacing_existing_records(self):
        toolkit = Resource.objects.get(slug="unhcr-suicide-prevention-toolkit")
        self.assertEqual(toolkit.published_year, 2022)
        self.assertEqual(
            toolkit.author_credit,
            "Obermeyer, M., Mukasa, M.B. and Ventevogel, P.",
        )
        self.assertIn("Existing source notes", toolkit.description)

        culture_resource = Resource.objects.get(
            slug="culture-context-mental-health-south-sudan-displacement"
        )
        self.assertEqual(
            culture_resource.author_credit,
            "Tankink, M. et al., including Mukasa, M.B.",
        )
        guide = Resource.objects.get(
            slug="integrating-mhpss-peacebuilding-programs-practical-guide"
        )
        self.assertEqual(guide.publisher, "Search for Common Ground")
        self.assertEqual(guide.author_credit, "Mukasa Bwesige, M. and contributors")

    def test_supplementary_professional_information_is_added_without_replacing_existing_records(self):
        home = self.client.get(reverse("home"))
        self.assertContains(home, "Global Mission-Oriented Transformation Protection Technical Specialist")
        self.assertContains(home, "Global Mission Transformation – Protection Specialist")
        self.assertContains(home, "over a decade of humanitarian experience")
        self.assertContains(home, "Inter-Regional MHPSS Officer for JRS’s Eastern and Southern Africa regions")

        about = self.client.get(reverse("about"))
        self.assertContains(about, "Global Mission-Oriented Transformation Protection Technical Specialist")
        self.assertContains(about, "Global Mission Transformation – Protection Specialist")
        self.assertContains(about, "strategic, technical and programmatic MHPSS advisory and on-site practice support")
        self.assertContains(about, "epistemic justice")
        self.assertContains(about, "Programme strategy, design and quality assurance")
        self.assertContains(about, "Prevention of Sexual Exploitation and Abuse (PSEA)")
        self.assertContains(about, "Swahili — basic")

        areas = self.client.get(reverse("areas"))
        self.assertContains(areas, "programme design and evaluation")
        self.assertContains(areas, "training, coaching and mentoring")
        self.assertContains(areas, "bidirectional integration of MHPSS")

        contact = self.client.get(reverse("contact"))
        for value in (
            "Independent MHPSS Technical Consultant",
            "Hunter St, Yeoville, Johannesburg, 2198, South Africa.",
            "Kilimani, Gitanga Road, Nairobi, Kenya.",
            "Department of Special Needs, Ghent University, Henri Dunantlaan 9, 9000 Ghent, Belgium.",
            "Makerere University College of Humanities and Social Sciences (CHUSS), School of Psychology, Uganda.",
            "mailto:moses.mukasa@ugent.be",
            "mailto:moses.mukasa@jrs.net",
            "tel:+256788926044",
            "tel:+32479033198",
            "https://www.linkedin.com/in/moses-mukasa-bwesige-6b2625183/",
            "@MBwesige",
            "@mukasa moses Bwesige",
        ):
            with self.subTest(value=value):
                self.assertContains(contact, value)

    def test_new_publication_records_have_conservative_attribution(self):
        for title in (
            "Culture, Context and Mental Health and Psychosocial Well-being of Refugees and Internally Displaced Persons from South Sudan",
            "Treatment Outcomes for Substance Use Disorders Across the African Continent: A Systematic Review",
            "Integrating MHPSS into Peacebuilding Programs: A Practical Guide",
            "Reflexive Training: Reimagining Trainers of Trainers in Mental Health and Psychosocial Support",
        ):
            with self.subTest(title=title):
                response = self.client.get(reverse("publications"), {"q": title})
                self.assertContains(response, title)

        institutional = self.client.get(
            reverse("publications"),
            {"q": "Culture, Context and Mental Health"},
        )
        self.assertContains(institutional, "Institutional publication")
        review = self.client.get(
            reverse("publications"),
            {"q": "Treatment Outcomes for Substance Use Disorders"},
        )
        self.assertContains(review, "BMC Psychology")
        book = self.client.get(
            reverse("publications"),
            {"q": "Reflexive Training"},
        )
        self.assertContains(book, "Moses Mukasa Bwesige")

    def test_unpublished_professional_experience_is_not_visible(self):
        ProfessionalExperience.objects.create(
            title="Private career draft",
            start_year=2010,
            is_published=False,
        )
        response = self.client.get(reverse("about"))
        self.assertNotContains(response, "Private career draft")

    def test_homepage_uses_all_six_published_themes_and_selected_research(self):
        response = self.client.get(reverse("home"))
        for title in (
            "Mental health and psychosocial support",
            "Suicide prevention and research",
            "Humanitarian and refugee mental health",
            "Community-led and culturally grounded support",
            "Mental health, conflict and peacebuilding",
            "Equitable collaboration and localisation",
        ):
            with self.subTest(theme=title):
                self.assertContains(response, title)
        self.assertContains(response, "Selected peer-reviewed work")
        self.assertContains(response, "Great Lakes Research Institute")
        self.assertContains(response, "approved professional portrait")
        self.assertContains(response, "Photographs to come")
        self.assertContains(
            response,
            "Webinar on Suicide prevention [09.04.2025, ENG]",
        )
        self.assertContains(response, "Вебінар: «Запобігання самогубствам» [09.04.2025, UKR]")
        self.assertContains(
            response,
            "Let&#x27;s talk life - Understanding Suicide and Promoting Mental Wellness",
        )
        self.assertContains(response, "2024-02-29")
        self.assertContains(response, "youtube-nocookie.com/embed/")
        self.assertNotContains(response, "autoplay")

    def test_homepage_includes_selected_uploaded_photographs_with_alt_text_and_captions(self):
        with tempfile.TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            MediaAppearance.objects.create(
                title="Research workshop in northern Uganda",
                summary="Facilitating a locally led research discussion.",
                source="Professional workshop",
                media_type=MediaAppearance.MediaType.PHOTO,
                is_published=True,
                is_featured=True,
                thumbnail=SimpleUploadedFile(
                    "research-workshop.jpg",
                    b"test-image-data",
                    content_type="image/jpeg",
                ),
                thumbnail_alt="Moses facilitating a research workshop in northern Uganda",
            )
            response = self.client.get(reverse("home"))

        self.assertContains(response, "Research workshop in northern Uganda")
        self.assertContains(response, "Moses facilitating a research workshop in northern Uganda")
        self.assertContains(response, "Facilitating a locally led research discussion.")
        self.assertContains(response, 'loading="lazy"')

    def test_homepage_links_external_video_items_without_embedding_them(self):
        MediaAppearance.objects.create(
            title="External training recording",
            media_type=MediaAppearance.MediaType.VIDEO,
            original_url="https://video.example.org/recordings/training",
            published_year=2026,
            is_published=True,
            is_featured=True,
        )
        response = self.client.get(reverse("home"))
        html = response.content.decode()

        self.assertContains(response, "External training recording")
        self.assertContains(response, "Open original media item")
        self.assertContains(response, "https://video.example.org/recordings/training")
        self.assertNotIn('src="https://video.example.org/recordings/training"', html)

    def test_area_detail_shows_related_research_and_source_links(self):
        response = self.client.get(
            reverse("area_detail", kwargs={"slug": "suicide-prevention-and-research"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Coping mechanisms adopted following a suicide attempt")
        self.assertContains(response, "Related contributions")
        self.assertContains(response, "Cambridge Prisms: Global Mental Health")

    def test_publication_archive_filters_by_type_year_topic_and_search(self):
        response = self.client.get(
            reverse("publications"),
            {
                "type": "research",
                "year": "2026",
                "topic": "suicide-prevention-and-research",
                "q": "coping",
                "publisher": "Cambridge University Press & Assessment",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Coping mechanisms adopted following a suicide attempt")
        self.assertNotContains(response, "Despair and Suicide-Related Behaviours")

    def test_media_archive_filters_and_paginates(self):
        filtered = self.client.get(reverse("media"), {"language": "uk"})
        self.assertContains(filtered, "Вебінар: «Запобігання самогубствам» [09.04.2025, UKR]")
        self.assertNotContains(filtered, "Webinar on Suicide prevention [09.04.2025, ENG]")
        publisher_filtered = self.client.get(reverse("media"), {"publisher": "MHPSS TWG Ukraine"})
        self.assertContains(publisher_filtered, "Webinar on Suicide prevention [09.04.2025, ENG]")
        self.assertNotContains(publisher_filtered, "Let&#x27;s talk life")
        kinyarwanda = self.client.get(reverse("media"), {"language": "rw"})
        self.assertContains(kinyarwanda, "Kinyarwanda")
        self.assertContains(kinyarwanda, "Regional training on mental health and peacebuilding in Kigali")
        second_page = self.client.get(reverse("media"), {"page": "2"})
        self.assertEqual(second_page.status_code, 200)
        self.assertContains(second_page, "Page 2 of 2")

    def test_public_content_pages_render_when_all_editorial_records_are_unpublished(self):
        for model in (WorkArea, Resource, MediaAppearance, ProfessionalExperience):
            model.objects.all().update(is_published=False)
        Insight.objects.all().update(is_published=False)
        for name in ("home", "about", "areas", "media", "publications", "insights"):
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_seo_endpoints(self):
        self.assertEqual(self.client.get(reverse("sitemap")).status_code, 200)
        robots = self.client.get(reverse("robots"))
        self.assertEqual(robots.status_code, 200)
        self.assertContains(robots, "Sitemap:")

    def test_custom_error_pages_render(self):
        self.assertEqual(self.client.get("/missing-page/").status_code, 404)


class ContactFormTests(TestCase):
    def test_valid_contact_submission_is_stored(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "A. Visitor",
                "email": "visitor@example.com",
                "subject": "Professional enquiry",
                "message": "I would like to discuss a professional collaboration.",
                "website": "",
            },
        )
        self.assertRedirects(response, reverse("contact"), fetch_redirect_response=False)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertContains(self.client.get(reverse("contact")), "Your message has been received")

    def test_contact_form_rejects_short_message_and_honeypot(self):
        base = {"name": "A. Visitor", "email": "visitor@example.com", "subject": "Enquiry"}
        short_message = ContactForm({**base, "message": "Too short", "website": ""})
        self.assertFalse(short_message.is_valid())
        self.assertIn("message", short_message.errors)
        spam = ContactForm({**base, "message": "A sufficiently long message", "website": "spam"})
        self.assertFalse(spam.is_valid())
        self.assertIn("website", spam.errors)

    def test_contact_submission_requires_csrf(self):
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post(reverse("contact"), {})
        self.assertEqual(response.status_code, 403)


class ContentModelTests(TestCase):
    def test_slug_is_generated_and_unique(self):
        first = WorkArea.objects.create(title="Community Mental Health")
        second = WorkArea.objects.create(title="Community Mental Health")
        self.assertEqual(first.slug, "community-mental-health")
        self.assertEqual(second.slug, "community-mental-health-2")

    def test_youtube_embed_is_converted_to_privacy_enhanced_host(self):
        item = MediaAppearance(
            title="Training",
            embed_url="https://www.youtube.com/watch?v=abc123xyz",
            published_on=date(2024, 1, 1),
        )
        self.assertEqual(item.privacy_embed_url, "https://www.youtube-nocookie.com/embed/abc123xyz")
        item.embed_url = "https://example.com/embed/abc123"
        self.assertEqual(item.privacy_embed_url, "")
