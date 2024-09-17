from django.urls import path

from .views import home_page_view, about_page_view

urlpatterns = [
    path("about/", about_page_view),
    path("", home_page_view),
]