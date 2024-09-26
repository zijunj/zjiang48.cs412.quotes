from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe

import time
import random

# lists for randomint
quotes = ["We cannot solve our problems with the same thinking we used when we created them.", "Two things are infinite: the universe and human stupidity; and I'm not sure about the universe.", "There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle."]
img = ["/static/img/albert_einstein.jpg","/static/img/albert_einstein2.jpg","/static/img/albert_einstein3.jpg"]

randInt = random.randint(0, 2)
quoteRandom= quotes[randInt]
imgRandom = img[randInt]


def home_page_view(request):
  template_name = 'quotes/base.html'

  context = {"quote": quoteRandom,
               "img": imgRandom,
               }
  return render(request, template_name, context)

def about_page_view(request):  
  template_name = 'quotes/about.html'

  context = {"quote": quoteRandom,
             "img": imgRandom,
          }
  
  return render(request, template_name, context)

def quote_page_view(request):
  template_name = 'quotes/quote.html'

  global quoteRandom, imgRandom

  randInt = random.randint(0, 2)
  quoteRandom = quotes[randInt]
  imgRandom = img[randInt]
  
  context = {"quote": quoteRandom,
               "img": imgRandom,

               }
  return render(request, template_name, context)

def show_all_page_view(request):  
  template_name = 'quotes/show_all.html'
  
  context = {"quote": quotes,
             "img": img,
             }
  return render(request, template_name, context)



