from orders.models import Order
from django.shortcuts import render, redirect
from django.contrib import messages
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
                messages.success(request, 'Данные обновлены')
            except ObjectDoesNotExist:
                customer = Customer.objects.create(
                    user=user,
                    phone=phone
                )
                user.first_name = name
                user.email = email
                user.save()
                messages.success(request, 'Профиль создан')

    customer_data = {
        'name': '',
        'phone': '',
        'email': '',
    }
    
    orders = []
    
    if request.user.is_authenticated:
        customer_data['name'] = request.user.first_name or request.user.username
        customer_data['email'] = request.user.email
        
        try:
            customer = Customer.objects.get(user=request.user)
            orders = Order.objects.filter(customer=customer)
            customer_data['phone'] = customer.phone
        except ObjectDoesNotExist:
            pass
    
    customer_json = json.dumps(customer_data)
    return render(request, 'lk.html', context={
        'orders': orders, 
        'customer_json': customer_json
    })


def login_by_phone(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        
        if not phone:
            messages.error(request, 'Введите номер телефона')
            return redirect('view_lk')
        
        try:
            customer = Customer.objects.get(phone=phone)
            
            if customer and customer.user:
                login(request, customer.user)
                messages.success(request, 'Вход выполнен успешно')
                return redirect('view_lk')
            else:
                messages.error(request, 'Пользователь не найден')
                
        except Customer.DoesNotExist:
            messages.error(request, 'Пользователь с таким номером не найден')
        
        return redirect('view_lk')
    
    return redirect('view_lk')
