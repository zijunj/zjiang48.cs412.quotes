from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

import time
from datetime import datetime, timedelta

import random


def base_page_view(request):
    '''
    Show base page
    '''
    template_name = 'restaurant/base.html'

    return render(request, template_name)

def main_page_view(request):
    '''
    Show main page
    '''
    template_name = 'restaurant/main.html'

    return render(request, template_name)


def submit(request):
    '''
    Handle the form submission.
    Read the form data from the request,
    and send it back to a template.
    '''

    template_name = 'restaurant/confirmation.html'
    
    # check that we have a POST request
    if request.POST:
        
        # item string
        items = ""
        # Subtotal price
        subtotal = 0
        
        # Read menu items and add to total
        
        if request.POST['chicken_alfredo']:
            items += "<li>Chicken Alfredo - $20.99 </li>" 
            subtotal += 20.99
        if request.POST['chicken_parm']:
            items += "<li>Chicken Parmigiana - $20.79 </li>" 
            subtotal += 20.79
        if request.POST['chicken_scampi']:
            items += "<li>Chicken Scampi - $21.49 </li>" 
            subtotal += 21.49
        if request.POST['tour_of_italy']:
            items += "<li>Tour Of Italy - $22.99 </li>" 
            subtotal += 22.99
        if request.POST['house_salad']:
            items += "<li>House Salad - $8.99 </li>" 
            subtotal += 8.99
            
        subtotal = round(subtotal,2)

        # Tax
        tax = round(subtotal * 0.0625, 2)
        
        # Total
        total = subtotal + tax
        
        # read the customer data into python variables
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']

        # random arrival time from 30min - 60 mins
        
        
        # package the form data up as context variables for the template
        context = {
            'items': mark_safe(items),
            'subtotal': subtotal,
            'total': total,
            'tax': tax,
            'name' : name,
            'phone': phone,
            'email': email,
        }

        return render(request, template_name, context)
    
    return redirect("order_page_view")

def order_page_view(request):
    '''
    Show order page
    '''
    template_name = 'restaurant/order.html'

    return render(request, template_name)

