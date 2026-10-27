from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import ContactForm
from .models import (
    Insight,
    MediaAppearance,
    Organization,
    Profile,
    ProfessionalExperience,
    Resource,
    WorkArea,
)


def home(request):
    resources = Resource.objects.filter(is_published=True).prefetch_related(
        "organizations",
        "related_areas",
    )
    featured_media = MediaAppearance.objects.filter(
        is_published=True,
        is_featured=True,
    )
    return render(
        request,
        "content/home.html",
        {
            "profile": Profile.objects.first(),
            "career_highlights": ProfessionalExperience.objects.filter(
                is_published=True,
                is_featured=True,
            ).order_by("sort_order"),
            "work_areas": WorkArea.objects.filter(is_published=True).order_by("order", "title"),
            "featured_research": resources.filter(
                resource_type=Resource.ResourceType.RESEARCH,
                is_featured=True,
            ).order_by("-published_year", "title")[:3],
            "institutional_resources": resources.exclude(
                resource_type=Resource.ResourceType.RESEARCH,
            ).order_by("-is_featured", "-published_year", "title")[:6],
            "organizations": Organization.objects.filter(
                is_published=True,
                is_featured=True,
            ).order_by("order", "title"),
            "featured_photos": featured_media.filter(
                media_type=MediaAppearance.MediaType.PHOTO,
            ).exclude(thumbnail="").order_by("order", "-published_year", "title")[:3],
            "featured_videos": featured_media.filter(
                media_type__in=(
                    MediaAppearance.MediaType.VIDEO,
                    MediaAppearance.MediaType.WEBINAR,
                    MediaAppearance.MediaType.TRAINING,
                ),
            )
            .filter(Q(embed_url__gt="") | Q(original_url__gt=""))
            .order_by("-published_year", "order", "title")[:3],
            "media_items": MediaAppearance.objects.filter(
                is_published=True,
                media_type__in=(
                    MediaAppearance.MediaType.INTERVIEW,
                    MediaAppearance.MediaType.FEATURE,
                    MediaAppearance.MediaType.CONFERENCE,
                ),
            ).prefetch_related("related_areas").order_by(
                "-published_year",
                "order",
            )[:5],
            "insights": Insight.objects.filter(is_published=True).order_by(
                "-published_on",
                "-published_year",
                "title",
            )[:2],
        },
    )


def about(request):
    profile = Profile.objects.prefetch_related("source_references").first()
    return render(
        request,
        "content/about.html",
        {
            "profile": profile,
            "about_references": (
                profile.source_references.filter(
                    publisher__in=(
                        "Jesuit Refugee Service USA",
                        "Great Lakes Research Institute for Mental Health & Wellbeing",
                    )
                )
                if profile
                else ()
            ),
            "professional_experience": ProfessionalExperience.objects.filter(
                is_published=True,
            )
            .prefetch_related("source_references")
            .order_by("sort_order"),
            "education_text": profile.qualifications if profile else "",
            "affiliations_text": profile.affiliations if profile else "",
            "research_records": Resource.objects.filter(
                is_published=True,
                resource_type=Resource.ResourceType.RESEARCH,
            ).order_by("-published_year", "title"),
            "selected_contributions": MediaAppearance.objects.filter(
                is_published=True,
                is_featured=True,
                media_type__in=(
                    MediaAppearance.MediaType.INTERVIEW,
                    MediaAppearance.MediaType.FEATURE,
                    MediaAppearance.MediaType.CONFERENCE,
                ),
            ).order_by("-published_year", "order", "title")[:4],
        },
    )


def areas(request):
    return render(
        request,
        "content/areas.html",
        {
            "work_areas": WorkArea.objects.filter(is_published=True)
            .prefetch_related("source_references")
            .order_by("order", "title")
        },
    )


def area_detail(request, slug):
    area = get_object_or_404(
        WorkArea.objects.filter(is_published=True).prefetch_related("source_references"),
        slug=slug,
    )
    return render(
        request,
        "content/area_detail.html",
        {
            "area": area,
            "resources": area.resources.filter(is_published=True)
            .prefetch_related("organizations")
            .order_by("-published_year", "title"),
            "media_items": area.media.filter(is_published=True).order_by(
                "-published_year",
                "order",
            ),
            "insights": area.insights.filter(is_published=True).order_by(
                "-published_on",
                "-published_year",
            ),
        },
    )


def publications(request):
    resources = Resource.objects.filter(is_published=True).prefetch_related(
        "organizations",
        "related_areas",
    )
    search = request.GET.get("q", "").strip()
    resource_type = request.GET.get("type", "")
    year = request.GET.get("year", "")
    topic = request.GET.get("topic", "")
    publisher = request.GET.get("publisher", "").strip()

    if search:
        resources = resources.filter(
            Q(title__icontains=search)
            | Q(summary__icontains=search)
            | Q(description__icontains=search)
            | Q(author_credit__icontains=search)
            | Q(publisher__icontains=search)
            | Q(source_attribution__icontains=search)
            | Q(journal_name__icontains=search)
            | Q(doi__icontains=search)
            | Q(organizations__title__icontains=search)
            | Q(related_areas__title__icontains=search)
        )
    if resource_type in Resource.ResourceType.values:
        resources = resources.filter(resource_type=resource_type)
    if year.isdigit():
        resources = resources.filter(published_year=int(year))
    if topic:
        resources = resources.filter(related_areas__slug=topic)
    if publisher:
        resources = resources.filter(publisher=publisher)
    resources = resources.distinct().order_by("-published_year", "title")
    page_obj = Paginator(resources, 6).get_page(request.GET.get("page"))

    return render(
        request,
        "content/publications.html",
        {
            "page_obj": page_obj,
            "resources": page_obj.object_list,
            "search": search,
            "selected_type": resource_type,
            "selected_year": year,
            "selected_topic": topic,
            "selected_publisher": publisher,
            "resource_types": Resource.ResourceType.choices,
            "publishers": Resource.objects.filter(is_published=True)
            .exclude(publisher="")
            .order_by("publisher")
            .values_list("publisher", flat=True)
            .distinct(),
            "years": Resource.objects.filter(
                is_published=True,
                published_year__isnull=False,
            )
            .order_by("-published_year")
            .values_list("published_year", flat=True)
            .distinct(),
            "topics": WorkArea.objects.filter(is_published=True).order_by("order", "title"),
        },
    )


def media(request):
    media_items = MediaAppearance.objects.filter(is_published=True).prefetch_related(
        "organizations",
        "related_areas",
    )
    search = request.GET.get("q", "").strip()
    media_type = request.GET.get("type", "")
    year = request.GET.get("year", "")
    language = request.GET.get("language", "")
    topic = request.GET.get("topic", "")
    publisher = request.GET.get("publisher", "").strip()

    if search:
        media_items = media_items.filter(
            Q(title__icontains=search)
            | Q(summary__icontains=search)
            | Q(description__icontains=search)
            | Q(source__icontains=search)
            | Q(related_areas__title__icontains=search)
        )
    if media_type in MediaAppearance.MediaType.values:
        media_items = media_items.filter(media_type=media_type)
    if year.isdigit():
        media_items = media_items.filter(published_year=int(year))
    if language in MediaAppearance.Language.values:
        media_items = media_items.filter(language=language)
    if topic:
        media_items = media_items.filter(related_areas__slug=topic)
    if publisher:
        media_items = media_items.filter(source=publisher)
    page_obj = Paginator(
        media_items.distinct().order_by("-is_featured", "-published_year", "order", "title"),
        8,
    ).get_page(request.GET.get("page"))

    return render(
        request,
        "content/media.html",
        {
            "page_obj": page_obj,
            "media_items": page_obj.object_list,
            "search": search,
            "selected_type": media_type,
            "selected_year": year,
            "selected_language": language,
            "selected_topic": topic,
            "selected_publisher": publisher,
            "media_types": MediaAppearance.MediaType.choices,
            "languages": MediaAppearance.Language.choices,
            "publishers": MediaAppearance.objects.filter(is_published=True)
            .exclude(source="")
            .order_by("source")
            .values_list("source", flat=True)
            .distinct(),
            "years": MediaAppearance.objects.filter(
                is_published=True,
                published_year__isnull=False,
            )
            .order_by("-published_year")
            .values_list("published_year", flat=True)
            .distinct(),
            "topics": WorkArea.objects.filter(is_published=True).order_by("order", "title"),
        },
    )


def insights(request):
    return render(
        request,
        "content/insights.html",
        {
            "insights": Insight.objects.filter(is_published=True)
            .prefetch_related("related_areas")
            .order_by("-published_on", "-published_year", "title")
        },
    )


@require_http_methods(["GET", "POST"])
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            client_key = f"contact-submission:{request.session.session_key or request.META.get('REMOTE_ADDR', 'unknown')}"
            if cache.get(client_key):
                form.add_error(None, "Please wait before sending another message.")
            else:
                form.save()
                cache.set(client_key, True, 60)
                messages.success(request, "Thank you. Your message has been received.")
                return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "content/contact.html", {"form": form})


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    return HttpResponse(f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {sitemap_url}\n", content_type="text/plain")
