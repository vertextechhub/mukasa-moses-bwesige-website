from django.contrib import admin

from .models import (
    ContactMessage,
    Insight,
    MediaAppearance,
    Organization,
    Profile,
    ProfessionalExperience,
    Resource,
    SourceReference,
    WorkArea,
)


class PublishedAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "is_featured", "order", "updated_at")
    list_filter = ("is_published", "is_featured")
    search_fields = ("title", "summary", "description", "source_attribution")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "title")
    date_hierarchy = "updated_at"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "updated_at")
    filter_horizontal = ("source_references",)
    fieldsets = (
        ("Profile", {"fields": ("full_name", "headline", "short_biography", "biography")}),
        ("Documented record", {"fields": ("experience", "qualifications", "affiliations", "source_references")}),
        ("Portrait", {"fields": ("portrait", "portrait_alt")}),
    )

    def has_add_permission(self, request):
        return not Profile.objects.exists()


@admin.register(ProfessionalExperience)
class ProfessionalExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "organization",
        "display_period",
        "evidence_status",
        "is_featured",
        "is_published",
        "sort_order",
    )
    list_filter = ("experience_type", "evidence_status", "is_featured", "is_published")
    search_fields = ("title", "organization", "location", "description", "evidence_note")
    filter_horizontal = ("source_references",)
    ordering = ("sort_order",)
    fieldsets = (
        (
            "Role",
            {
                "fields": (
                    "title",
                    "organization",
                    "location",
                    "experience_type",
                    "description",
                )
            },
        ),
        (
            "Dates and evidence",
            {
                "fields": (
                    "start_month",
                    "start_year",
                    "end_month",
                    "end_year",
                    "period_note",
                    "evidence_status",
                    "evidence_note",
                    "source_references",
                )
            },
        ),
        ("Publishing", {"fields": ("sort_order", "is_featured", "is_published")}),
    )


@admin.register(WorkArea)
class WorkAreaAdmin(PublishedAdmin):
    filter_horizontal = ("source_references",)
    fieldsets = (
        ("Theme", {"fields": ("title", "slug", "summary", "description", "order")}),
        ("Evidence", {"fields": ("source_url", "source_attribution", "source_references")}),
        ("Publishing", {"fields": ("is_published", "is_featured")}),
    )


@admin.register(Resource)
class ResourceAdmin(PublishedAdmin):
    list_display = ("title", "resource_type", "published_year", "published_on", "is_published", "is_featured", "order")
    list_filter = ("resource_type", "publisher", "published_year", "is_published", "is_featured", "language")
    search_fields = PublishedAdmin.search_fields + ("author_credit", "publisher", "doi", "journal_name")
    filter_horizontal = ("organizations", "source_references", "related_areas")
    fieldsets = (
        ("Content", {"fields": ("title", "slug", "summary", "description", "order")}),
        ("Bibliographic record", {"fields": ("resource_type", "author_credit", "publisher", "journal_name", "volume", "issue", "page_range", "doi", "published_on", "published_year", "language")}),
        ("Sources and topics", {"fields": ("source_url", "source_attribution", "organizations", "source_references", "related_areas")}),
        ("Publishing", {"fields": ("is_published", "is_featured")}),
    )


@admin.register(MediaAppearance)
class MediaAppearanceAdmin(PublishedAdmin):
    list_display = ("title", "media_type", "language", "published_year", "published_on", "is_published", "is_featured", "order")
    list_filter = ("media_type", "source", "language", "published_year", "is_published", "is_featured")
    search_fields = PublishedAdmin.search_fields + ("source", "original_url", "source_url")
    filter_horizontal = ("organizations", "source_references", "related_areas")
    fieldsets = (
        (
            "Content",
            {
                "fields": ("title", "slug", "summary", "description", "order"),
                "description": "For photographs, use Summary as the caption shown with the image.",
            },
        ),
        ("Appearance details", {"fields": ("media_type", "language", "source", "published_on", "published_year")}),
        ("Original links and topics", {"fields": ("source_url", "original_url", "embed_url", "organizations", "source_references", "related_areas")}),
        (
            "Photo or video thumbnail",
            {
                "fields": ("thumbnail", "thumbnail_alt"),
                "description": "For a published Photograph, upload the image here and provide descriptive alternative text.",
            },
        ),
        ("Publishing", {"fields": ("is_published", "is_featured")}),
    )


@admin.register(Insight)
class InsightAdmin(PublishedAdmin):
    list_display = ("title", "published_on", "is_published", "order")
    filter_horizontal = ("source_references", "related_areas")
    fieldsets = (
        ("Content", {"fields": ("title", "slug", "summary", "description", "order")}),
        ("Publication", {"fields": ("published_on", "published_year", "original_source", "source_url", "source_references", "related_areas")}),
        ("Publishing", {"fields": ("is_published", "is_featured")}),
    )


@admin.register(Organization)
class OrganizationAdmin(PublishedAdmin):
    list_display = ("title", "website_url", "is_published")


@admin.register(SourceReference)
class SourceReferenceAdmin(admin.ModelAdmin):
    list_display = ("title", "publisher", "published_on", "verification_status")
    search_fields = ("title", "publisher", "url", "notes")
    list_filter = ("verification_status", "published_on")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "received_at", "is_read")
    list_filter = ("is_read", "received_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "received_at")
    actions = ("mark_read",)

    @admin.action(description="Mark selected messages as read")
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)
