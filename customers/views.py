from orders.models import Order
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

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
            return redirect('lk')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def view_lk(request):
    user = request.user

    if request.method == 'POST':
        phone = request.POST.get('phone')
        name = request.POST.get('first_name')
        email = request.POST.get('email')
        
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
    context = {}
    if user.is_authenticated:
        try:
            customer = Customer.objects.get(user=user)
            context = {
                'user': user,
                'customer': customer,
                'orders': customer.orders.all(),
            }
        except Customer.DoesNotExist:
            context = {
                'user': user,
                'customer': None,
                'orders': [],
            }

    return render(request, 'lk.html', context=context)
