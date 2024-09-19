from django.http import HttpResponse
from django.shortcuts import render
import time
import random

quotes = ["We cannot solve our problems with the same thinking we used when we created them.", "Tact is the art of making a point without making an enemy.", "A man who dares to waste one hour of time has not discovered the value of life."]
names = ["Albert Einstein", "Issac Newton", "Charles Darwin"]
img = ["","",""]

randInt = random.randint(0, 2)
quoteRandom = quotes[randInt]
nameRandom = names[randInt]
imgRandom = img[randInt]


def home_page_view(request):
  template_name = 'quotes/quote.html'

  context = {"quote": quoteRandom,
               "name": nameRandom,             
               "img": imgRandom
               }
  return render(request, template_name, context)

def about_page_view(request):  
  context = {"quote": quoteRandom,
               "name": nameRandom,             
               "img": imgRandom
               }
  return render(request, "quotes/about.html", context)

def quote_page_view(request):
  context = {"quote": quoteRandom,
               "name": nameRandom,             
               "img": imgRandom
               }
  return render(request, "", context)

def base_view(request):
  return render (request, "quotes/base.html")

