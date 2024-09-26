from django.urls import path

from django.conf import settings

from . import views


urlpatterns = [
    path(r'', views.quote_page_view, name="home"),
    path(r' quote', views.quote_page_view, name="quote"),
    path(r'about', views.about_page_view, name="about"),
    path(r'show_all', views.show_all_page_view, name="show_all"),

]

