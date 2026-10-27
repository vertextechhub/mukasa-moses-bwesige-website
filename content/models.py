from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class PublishedContent(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    summary = models.CharField(max_length=320, blank=True)
    description = models.TextField(blank=True)
    source_url = models.URLField(blank=True)
    source_attribution = models.CharField(max_length=220, blank=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    published_year = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("order", "title")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:200] or self.__class__.__name__.lower()
            candidate = base_slug
            suffix = 2
            while self.__class__.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                candidate = f"{base_slug[:210 - len(str(suffix))]}-{suffix}"
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)


class Profile(models.Model):
    full_name = models.CharField(max_length=160, default="Mukasa Moses Bwesige")
    headline = models.CharField(max_length=220, blank=True)
    short_biography = models.TextField(blank=True)
    biography = models.TextField(blank=True)
    experience = models.TextField(blank=True, help_text="Add only verified professional experience.")
    qualifications = models.TextField(blank=True, help_text="Add only verified qualifications.")
    affiliations = models.TextField(blank=True, help_text="Add only verified affiliations.")
    portrait = models.ImageField(upload_to="portraits/", blank=True)
    portrait_alt = models.CharField(max_length=220, blank=True)
    source_references = models.ManyToManyField(
        "SourceReference",
        blank=True,
        related_name="profiles",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "professional profile"
        verbose_name_plural = "professional profile"

    def __str__(self):
        return self.full_name

    def clean(self):
        if self.portrait and not self.portrait_alt.strip():
            raise ValidationError({"portrait_alt": "Provide meaningful alternative text for the portrait."})


class WorkArea(PublishedContent):
    source_references = models.ManyToManyField(
        "SourceReference",
        blank=True,
        related_name="work_areas",
    )

    class Meta(PublishedContent.Meta):
        abstract = False
        verbose_name = "area of work"
        verbose_name_plural = "areas of work"


class Organization(PublishedContent):
    website_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to="organisations/", blank=True)
    logo_alt = models.CharField(max_length=220, blank=True)

    class Meta(PublishedContent.Meta):
        abstract = False
        verbose_name = "organisation"
        verbose_name_plural = "organisations"

    def clean(self):
        if self.logo and not self.logo_alt.strip():
            raise ValidationError({"logo_alt": "Provide meaningful alternative text for the logo."})


class SourceReference(models.Model):
    class VerificationStatus(models.TextChoices):
        UNVERIFIED = "unverified", "Unverified"
        CONFIRMED = "confirmed", "Confirmed"
        NEEDS_REVIEW = "needs_review", "Needs review"
        UNAVAILABLE = "unavailable", "Unavailable"

    title = models.CharField(max_length=220)
    url = models.URLField(validators=[URLValidator(schemes=["http", "https"])])
    publisher = models.CharField(max_length=220, blank=True)
    published_on = models.DateField(null=True, blank=True)
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.UNVERIFIED,
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title


class ProfessionalExperience(models.Model):
    class ExperienceType(models.TextChoices):
        EMPLOYMENT = "employment", "Employment"
        CONSULTANCY = "consultancy", "Consultancy / project"
        VOLUNTEER = "volunteer", "Volunteer"
        GOVERNANCE = "governance", "Board / governance"
        PEER_SUPPORT = "peer_support", "Peer support"

    class EvidenceStatus(models.TextChoices):
        PROFILE_DOSSIER = "profile_dossier", "Supplied profile dossier"
        SOURCE_SUPPORTED = "source_supported", "Supported by a public source"
        NEEDS_CONFIRMATION = "needs_confirmation", "Needs identity or date confirmation"

    title = models.CharField(max_length=220)
    organization = models.CharField(max_length=220, blank=True)
    location = models.CharField(max_length=220, blank=True)
    experience_type = models.CharField(
        max_length=20,
        choices=ExperienceType.choices,
        default=ExperienceType.EMPLOYMENT,
    )
    start_year = models.PositiveSmallIntegerField(null=True, blank=True)
    start_month = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=tuple((month, month) for month in range(1, 13)),
    )
    end_year = models.PositiveSmallIntegerField(null=True, blank=True)
    end_month = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=tuple((month, month) for month in range(1, 13)),
    )
    period_note = models.CharField(
        max_length=220,
        blank=True,
        help_text="Use when source date precision is limited or dates conflict.",
    )
    description = models.TextField(blank=True)
    evidence_status = models.CharField(
        max_length=24,
        choices=EvidenceStatus.choices,
        default=EvidenceStatus.PROFILE_DOSSIER,
    )
    evidence_note = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    source_references = models.ManyToManyField(
        SourceReference,
        blank=True,
        related_name="professional_experiences",
    )

    class Meta:
        ordering = ("sort_order", "start_year", "start_month", "title")
        verbose_name = "professional experience"
        verbose_name_plural = "professional experience"

    def __str__(self):
        return f"{self.title} — {self.organization}" if self.organization else self.title

    @property
    def display_period(self):
        if self.period_note:
            return self.period_note
        if not self.start_year:
            return "Date not stated"

        start = self._format_date(self.start_year, self.start_month)
        if self.end_year:
            end = self._format_date(self.end_year, self.end_month)
        else:
            end = "present"
        return f"{start} – {end}"

    @staticmethod
    def _format_date(year, month):
        if month:
            from calendar import month_abbr

            return f"{month_abbr[month]} {year}"
        return str(year)


class Resource(PublishedContent):
    class ResourceType(models.TextChoices):
        RESEARCH = "research", "Research paper"
        TOOLKIT = "toolkit", "Toolkit"
        REPORT = "report", "Report"
        FEATURE = "feature", "Institutional feature"
        TRAINING = "training", "Training / educational resource"
        ARTICLE = "article", "Article"
        OTHER = "other", "Other resource"

    resource_type = models.CharField(max_length=20, choices=ResourceType.choices, default=ResourceType.OTHER)
    author_credit = models.CharField(max_length=500, blank=True)
    publisher = models.CharField(max_length=220, blank=True)
    doi = models.CharField(max_length=120, blank=True)
    journal_name = models.CharField(max_length=220, blank=True)
    volume = models.CharField(max_length=50, blank=True)
    issue = models.CharField(max_length=50, blank=True)
    page_range = models.CharField(max_length=40, blank=True)
    published_on = models.DateField(null=True, blank=True)
    language = models.CharField(max_length=40, blank=True)
    organizations = models.ManyToManyField(Organization, blank=True, related_name="resources")
    source_references = models.ManyToManyField(SourceReference, blank=True, related_name="resources")
    related_areas = models.ManyToManyField(WorkArea, blank=True, related_name="resources")

    class Meta(PublishedContent.Meta):
        abstract = False
        verbose_name = "publication or resource"
        verbose_name_plural = "publications and resources"


class MediaAppearance(PublishedContent):
    class MediaType(models.TextChoices):
        INTERVIEW = "interview", "Interview"
        FEATURE = "feature", "News / feature"
        WEBINAR = "webinar", "Webinar"
        TRAINING = "training", "Recorded training"
        CONFERENCE = "conference", "Conference contribution"
        VIDEO = "video", "Video"
        PHOTO = "photo", "Photograph"
        OTHER = "other", "Other media"

    class Language(models.TextChoices):
        ENGLISH = "en", "English"
        UKRAINIAN = "uk", "Ukrainian"
        KINYARWANDA = "rw", "Kinyarwanda"
        OTHER = "other", "Other / not specified"

    media_type = models.CharField(max_length=20, choices=MediaType.choices, default=MediaType.OTHER)
    language = models.CharField(max_length=8, choices=Language.choices, default=Language.ENGLISH)
    published_on = models.DateField(null=True, blank=True)
    source = models.CharField(max_length=220, blank=True)
    original_url = models.URLField(blank=True)
    embed_url = models.URLField(blank=True, help_text="Optional YouTube URL. Only YouTube embeds are enabled.")
    thumbnail = models.ImageField(upload_to="media-thumbnails/", blank=True)
    thumbnail_alt = models.CharField(max_length=220, blank=True)
    organizations = models.ManyToManyField(Organization, blank=True, related_name="media")
    source_references = models.ManyToManyField(SourceReference, blank=True, related_name="media")
    related_areas = models.ManyToManyField(WorkArea, blank=True, related_name="media")

    class Meta(PublishedContent.Meta):
        abstract = False
        verbose_name = "media appearance"
        verbose_name_plural = "media and speaking"

    def clean(self):
        super().clean()
        if self.thumbnail and not self.thumbnail_alt.strip():
            raise ValidationError({"thumbnail_alt": "Provide meaningful alternative text for the thumbnail."})
        if self.embed_url:
            from urllib.parse import urlparse

            host = urlparse(self.embed_url).hostname or ""
            if host.lower() not in {"youtube.com", "www.youtube.com", "youtu.be", "www.youtube-nocookie.com"}:
                raise ValidationError({"embed_url": "Use a YouTube URL; other media should be linked externally."})

    @property
    def privacy_embed_url(self):
        if not self.embed_url:
            return ""
        from urllib.parse import parse_qs, urlparse

        parsed = urlparse(self.embed_url)
        if parsed.hostname not in {
            "youtube.com",
            "www.youtube.com",
            "youtu.be",
            "www.youtu.be",
            "www.youtube-nocookie.com",
        }:
            return ""
        video_id = ""
        if parsed.hostname in {"youtu.be", "www.youtu.be"}:
            video_id = parsed.path.strip("/")
        elif parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]
        elif parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/embed/", 1)[1].split("/", 1)[0]
        if not video_id or not all(char.isalnum() or char in "-_" for char in video_id):
            return ""
        return f"https://www.youtube-nocookie.com/embed/{video_id}"


class Insight(PublishedContent):
    published_on = models.DateField(null=True, blank=True)
    original_source = models.CharField(max_length=220, blank=True)
    source_references = models.ManyToManyField(SourceReference, blank=True, related_name="insights")
    related_areas = models.ManyToManyField(WorkArea, blank=True, related_name="insights")

    class Meta(PublishedContent.Meta):
        abstract = False
        verbose_name = "insight"
        verbose_name_plural = "insights"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=160)
    message = models.TextField(max_length=5000)
    received_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("-received_at",)

    def __str__(self):
        return f"{self.subject} — {self.name}"
