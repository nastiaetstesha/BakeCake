from django.shortcuts import render
from catalog.models import Option


def index(request):
    ctx = {
        'levels':  Option.objects.filter(category__slug='levels',  is_active=True).order_by('id'),
        'shapes':  Option.objects.filter(category__slug='shape',   is_active=True).order_by('id'),
        'toppings':Option.objects.filter(category__slug='topping', is_active=True).order_by('id'),
        'berries': Option.objects.filter(category__slug='berries', is_active=True).order_by('id'),
        'decors':  Option.objects.filter(category__slug='decor',   is_active=True).order_by('id'),
    }
    return render(request, 'index.html', ctx)



# def cake_customization(request):
#     option_category = OptionCategory.objects.get(slug='levels')

#     option_name = Option.objects.filter(
#     return render(request, 'cake_customization.html', context)