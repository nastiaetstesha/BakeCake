from django.shortcuts import render
# from models import *


def index(request):
    return render(request, 'index.html')


# def cake_customization(request):
#     option_category = OptionCategory.objects.get(slug='levels')

#     option_name = Option.objects.filter(
#     return render(request, 'cake_customization.html', context)