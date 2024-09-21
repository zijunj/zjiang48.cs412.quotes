from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe

import time
import random

quotes = ["We cannot solve our problems with the same thinking we used when we created them.", "Tact is the art of making a point without making an enemy.", "A man who dares to waste one hour of time has not discovered the value of life."]
names = ["Albert Einstein", "Sir Issac Newton", "Charles Darwin"]
img = ["/static/img/albert_einstein.jpg","/static/img/issac_newton.jpg","/static/img/charles_darwin.jpg"]
aboutImg = ["https://upload.wikimedia.org/wikipedia/commons/3/3e/Einstein_1921_by_F_Schmutzer_-_restoration.jpg","https://upload.wikimedia.org/wikipedia/commons/3/3b/Portrait_of_Sir_Isaac_Newton%2C_1689.jpg","/static/img/charles_darwin2.jpg" ]
pElem = [mark_safe("<p>Albert Einstein (1879-1955) was a renowned theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics. His work is also known for its influence on the philosophy of science.</p> <p>Einstein is best known to the general public for his mass–energy equivalence formula E = mc². He received the Nobel Prize in Physics for his services to Theoretical Physics and his discovery of the law of the photoelectric effect.</p> <p>Einstein published more than 300 scientific papers and over 150 non-scientific works. His intellectual achievements and originality have made the word \"Einstein\" synonymous with \"genius\".</p>"),
         mark_safe("<p>Sir Isaac Newton (1642-1726/27) was an English physicist, mathematician, astronomer, and author who is widely recognized as one of the most influential scientists of all time and a key figure in the scientific revolution.</p> <p> Newton's book \"Philosophiæ Naturalis Principia Mathematica\" (Mathematical Principles of Natural Philosophy), first published in 1687, laid the foundations of classical mechanics. He also made seminal contributions to optics and shares credit with Gottfried Wilhelm Leibniz for developing infinitesimal calculus.</p> <p>Among his many achievements, Newton developed the theory that all colors are mixtures of Red, Green, and Blue light, resulting in the first known color circle in 1666[3]. His work on the laws of motion and universal gravitation formed the dominant scientific viewpoint until it was superseded by Einstein's theory of relativity.</p>"),
         mark_safe("<p>Charles Darwin (1809-1882) was an English naturalist, geologist, and biologist, best known for his contributions to the science of evolution. His proposition that all species of life have descended from common ancestors is now widely accepted and considered a fundamental concept in science.</p> <p>Darwin published his theory of evolution with compelling evidence in his 1859 book \"On the Origin of Species\". This work introduced the scientific theory that populations evolve over generations through a process of natural selection.</p> <p>Darwin's scientific discovery is the unifying theory of the life sciences, explaining the diversity of life. His work laid the foundation for modern evolutionary biology and has had a profound impact on many fields of science.</p>")]



randInt = random.randint(0, 2)
quoteRandom= quotes[randInt]
nameRandom = names[randInt]
imgRandom = img[randInt]
aboutimgRandom = aboutImg[randInt]
pElemRandom = pElem[randInt]


def home_page_view(request):
  template_name = 'quotes/quote.html'

  context = {"quote": quoteRandom,
               "name": nameRandom,             
               "img": imgRandom,
               "aboutImg": aboutimgRandom,
                "pElems": pElemRandom
               }
  return render(request, template_name, context)

def about_page_view(request):  
  template_name = 'quotes/about.html'


  context = {"quote": quoteRandom,
             "name": nameRandom,             
             "img": imgRandom,
             "aboutImg": aboutimgRandom,
             "pElems": pElemRandom

               }
  return render(request, template_name, context)

def quote_page_view(request):
  template_name = 'quotes/quote.html'

  global quoteRandom, nameRandom, imgRandom, aboutimgRandom, pElemRandom

  randInt = random.randint(0, 2)
  quoteRandom = quotes[randInt]
  nameRandom = names[randInt]
  imgRandom = img[randInt]
  aboutimgRandom = aboutImg[randInt]
  pElemRandom = pElem[randInt]
  
  

  context = {"quote": quoteRandom,
               "name": nameRandom,             
               "img": imgRandom,
               "aboutImg": aboutimgRandom,
               "pElems": pElemRandom

               }
  return render(request, template_name, context)

def show_all_page_view(request):  
  template_name = 'quotes/show_all.html'
  
  context = {"quote": quotes,
             "name": names,             
             "img": img,
             "aboutImg": aboutImg,
             "pElems": pElem
             }
  return render(request, template_name, context)



