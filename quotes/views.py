from django.http import HttpResponse
from django.shortcuts import render

def home_page_view(request):
    return HttpResponse("Homepage")

def about_page_view(request):  
    context = {"name": "Zi Jun"}
    return render(request, "quotes/about.html", context)

