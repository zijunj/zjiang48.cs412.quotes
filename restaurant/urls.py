from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'main/', views.main_page_view, name="main"),
    path(r'main/', views.base_page_view, name="base"),
    path(r'order/', views.order_page_view, name="order"),
    path(r'submit/', views.submit, name="submit"),


]

