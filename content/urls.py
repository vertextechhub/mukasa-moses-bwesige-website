from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("areas-of-work/", views.areas, name="areas"),
    path("areas-of-work/<slug:slug>/", views.area_detail, name="area_detail"),
    path("media-and-speaking/", views.media, name="media"),
    path("publications-and-resources/", views.publications, name="publications"),
    path("insights/", views.insights, name="insights"),
    path("contact/", views.contact, name="contact"),
    path("robots.txt", views.robots_txt, name="robots"),
]
