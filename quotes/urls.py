from django.urls import path

# from .views import home_page_view, about_page_view

from django.conf import settings

from . import views

# urlpatterns = [
#     path("about/", about_page_view),
#     path("", home_page_view),
# ]

urlpatterns = [
    path(r'', views.home_page_view, name="home"),
    path(r'', views.base_view, name="base"),
    path("about/", views.about_page_view, name="about"),

]

