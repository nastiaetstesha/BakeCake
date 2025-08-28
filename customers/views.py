from orders.models import Order
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import json

from .forms import SignUpForm
from .models import Customer


@transaction.atomic
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone = getattr(user, '_deferred_customer_phone', '')
            if phone and not hasattr(user, 'customer'):
                Customer.objects.create(user=user, phone=phone)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def view_lk(request):
    reg = request.GET.get('reg')
    if reg:
        try:
            customer = Customer.objects.get(phone=reg)
            if customer and customer.user:
                login(request, customer.user)
        except ObjectDoesNotExist:
            pass
    
    if request.method == 'POST':
        phone = request.POST.get('PHONE')
        name = request.POST.get('NAME')
        email = request.POST.get('EMAIL')
        user = request.user
        
        if user.is_authenticated:
            try:
                customer = Customer.objects.get(user=user)
                customer.phone = phone
                customer.save()
                
                user.first_name = name
                user.email = email
                user.save()
            except ObjectDoesNotExist:
                # Если у пользователя нет Customer профиля, создаем его
                customer = Customer.objects.create(
                    user=user,
                    phone=phone
                )
                user.first_name = name
                user.email = email
                user.save()

    customer_data = {
        'name': '',
        'phone': '',
        'email': '',
    }
    
    user = request.user
    if user.is_authenticated:
        customer_data['name'] = user.first_name or user.username
        customer_data['email'] = user.email
        
        try:
            customer = Customer.objects.get(user=user)
            orders = Order.objects.filter(customer=customer)
            customer_data['phone'] = customer.phone
            
            customer_json = json.dumps(customer_data)
            return render(request, 'lk.html', context={
                'orders': orders, 
                'customer_json': customer_json
            })
        except ObjectDoesNotExist:
            # Если у пользователя нет Customer профиля
            customer_json = json.dumps(customer_data)
            return render(request, 'lk.html', context={'customer_json': customer_json})
    
    customer_json = json.dumps(customer_data)
    return render(request, 'lk.html', context={'customer_json': customer_json})
