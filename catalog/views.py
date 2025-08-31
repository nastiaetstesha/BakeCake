from django.shortcuts import render
from catalog.models import Option, Cake


def serialize_cake(cake):
    return {
        'title': cake.title,
        'description': cake.description,
        'price': cake.base_price,
        'image': cake.image.url if cake.image else None
    }


def index(request):
    cakes = Cake.objects.all()
    serialized_cakes = [serialize_cake(cake) for cake in cakes]
    
    ctx = {
        'levels':  Option.objects.filter(category__slug='levels',  is_active=True).order_by('id'),
        'shapes':  Option.objects.filter(category__slug='shape',   is_active=True).order_by('id'),
        'toppings': Option.objects.filter(category__slug='topping', is_active=True).order_by('id'),
        'berries': Option.objects.filter(category__slug='berries', is_active=True).order_by('id'),
        'decors':  Option.objects.filter(category__slug='decor',   is_active=True).order_by('id'),
        'cakes': serialized_cakes,
    }
    return render(request, 'index.html', ctx)