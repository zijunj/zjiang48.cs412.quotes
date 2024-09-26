from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from datetime import datetime, timedelta

import random
from random import randint

daily_special = ["<img src=\"/static/img/chicken_alfredo.png\" alt=\"chicken_alfredo\"> <h3>Chicken Alfredo - Daily Special!</h3> <p>Our signature pasta dish with homemade Alfredo sauce</p> <div class=\"button-group\"> <button class=\"add-to-cart\" type= button\" ><input type=\"checkbox\" name=\"chicken_alfredo\"> Add to Cart - $19.99</button> <button class=\"add-options\" type=\"button\" ><input type=\"checkbox\" name=\"soup\"> Add Soup - Free</button> </div>",
                 "<img src=\"/static/img/chicken_and_shrimp_carbonara.png\" alt=\"chicken_and_shrimp\"> <h3>Chicken and Shrimp Carbonara - Daily Special!</h3> <p> Sautéed seasoned chicken, shrimp and spaghetti tossed in a creamy sauce with bacon and roasted red peppers. </p> <div class=\"button-group\"> <button class=\"add-to-cart\" type= button\" ><input type=\"checkbox\" name=\"chicken_and_shrimp\"> Add to Cart - $19.99</button> <button class=\"add-options\" type=\"button\" ><input type=\"checkbox\" name=\"soup\"> Add Soup - Free</button> </div>",
                 "<img src=\"/static/img/chicken_marsala_fettuccine.png\" alt=\"chicken_marsala\"> <h3>Chicken Marsala Fettuccine - Daily Special!</h3> <p> Chicken sautéed with spinach and mushrooms in a creamy marsala mushroom sauce. Served over fettuccine. </p> <div class=\"button-group\"> <button class=\"add-to-cart\" type= button\" ><input type=\"checkbox\" name=\"chicken_marsala\"> Add to Cart - $19.99</button> <button class=\"add-options\" type=\"button\" ><input type=\"checkbox\" name=\"soup\"> Add Soup - Free</button> </div>"]



def base_page_view(request):
    '''
    Show base page
    '''
    template_name = 'restaurant/base.html'

    return render(request, template_name)
def order_page_view(request):
    '''
    Show order page, picks a random daily special order
    '''
    template_name = 'restaurant/order.html'
    context = {
        'daily_special': mark_safe(daily_special[randint(0,2)])
    }

    return render(request, template_name, context)

def main_page_view(request):
    '''
    Show main page
    '''
    template_name = 'restaurant/main.html'

    return render(request, template_name)


def confirmation(request):
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
        # Subtotal and total price
        subtotal = 0
        total = 0
        
        # Read menu items and add to total
                        
        for key, value in request.POST.items():
            if key == 'chicken_alfredo':
                items += "<li>Chicken Alfredo - $19.99 </li>" 
                subtotal += 19.99
            if key == 'chicken_and_shrimp':
                items += "<li>Chicken and Shrimp Carbonara - $19.99 </li>" 
                subtotal += 19.99
            if key == 'chicken_marsala':
                items += "<li>Chicken Marsala Fettuccine - $19.99 </li>" 
                subtotal += 19.99
            if key == 'chicken_parm':
                items += "<li>Chicken Parmigiana - $20.79 </li>" 
                subtotal += 20.79
            if key == 'chicken_scampi':
                items += "<li>Chicken Scampi - $21.49 </li>" 
                subtotal += 21.49
            if key == 'tour_of_italy':
                items += "<li>Tour Of Italy - $22.99 </li>" 
                subtotal += 22.99
            if key == 'house_salad':
                items += "<li>House Salad - $8.99 </li>" 
                subtotal += 8.99
            if key == 'soup':
                items += "<li>Soup - Free!</li>" 

            
        subtotal = round(subtotal,2)

        # Tax
        tax = round(subtotal * 0.0625, 2)
        
        # Total
        total = round(subtotal + tax, 2)
        
        # read the customer data into python variables
        special_instructions = request.POST['special_instructions']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']

        # Get the current time
        current_time = datetime.now()

        # Generate a random duration between 30 and 60 minutes
        random_minutes = random.randint(30, 60)

        # Calculate the expected ready time
        expected_ready_time = current_time + timedelta(minutes=random_minutes)
        
        # Random order number 
        order_number = randint(100000,999999)
        
        
        # package the form data up as context variables for the template
        context = {
            'special_instructions': special_instructions,
            'order_number': order_number,
            'time': expected_ready_time,
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



