from django.shortcuts import render
from catalog.models import Option, Cake

import json


def serialize_cake(cake):
    return {
        'id': cake.id,
        'title': cake.title,
        'description': cake.description,
        'price': float(cake.base_price),
        'image': cake.image.url if cake.image else None
    }


def index(request):
    cakes = Cake.objects.all()
    serialized_cakes = [serialize_cake(cake) for cake in cakes]

    selected_cake = None
    selected_cake_id = request.GET.get('selected_cake')

    if selected_cake_id:
        try:
            selected_cake = Cake.objects.get(id=selected_cake_id)
        except Cake.DoesNotExist:
            selected_cake = None

    ctx = {
        'levels':  Option.objects.filter(category__slug='levels',  is_active=True).order_by('id'),
        'shapes':  Option.objects.filter(category__slug='shape',   is_active=True).order_by('id'),
        'toppings': Option.objects.filter(category__slug='topping', is_active=True).order_by('id'),
        'berries': Option.objects.filter(category__slug='berries', is_active=True).order_by('id'),
        'decors':  Option.objects.filter(category__slug='decor',   is_active=True).order_by('id'),
        'cakes': serialized_cakes,
        'selected_cake': selected_cake,
        'selected_cake_json': json.dumps(serialize_cake(selected_cake)) if selected_cake else 'null',
    }
    return render(request, 'index.html', ctx)
