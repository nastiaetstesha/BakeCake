from decimal import Decimal
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Order, OrderItem


@require_POST
def create(request):

    name = (request.POST.get('NAME') or '').strip()
    phone = (request.POST.get('PHONE') or '').strip()
    email = (request.POST.get('EMAIL') or '').strip()
    address = (request.POST.get('ADDRESS') or '').strip()
    delivery_date = parse_date(request.POST.get('DATE') or '') or timezone.now().date()
    # обязательные селекты по ТЗ
    levels_id = request.POST.get('LEVELS')
    shape_id = request.POST.get('FORM')
    topping_id = request.POST.get('TOPPING')

    if not all([name, phone, address, levels_id, shape_id, topping_id]):
        return HttpResponseBadRequest('Не заполнены обязательные поля.')

    order = Order.objects.create(
        contact_name=name,
        phone=phone,
        email=email,
        city='',
        street=address,
        house='',
        apartment='',
        delivery_comment=(request.POST.get('DELIVCOMMENTS') or '').strip(),
        delivery_date=delivery_date,
        consent_personal_data=True,
    )

    item = OrderItem.objects.create(
        order=order,
        cake=None,
        levels_id=levels_id,
        shape_id=shape_id,
        topping_id=topping_id,
        berry_id=request.POST.get('BERRIES') or None,
        decor_id=request.POST.get('DECOR') or None,
        inscription_text=(request.POST.get('WORDS') or '').strip(),
    )

    order.recalc_totals(save=True)

    return redirect('lk')

# это для расчета стоимости живой в углу страницы
@require_POST
def price(request):
    fake = OrderItem(
        levels_id=request.POST.get('LEVELS') or None,
        shape_id=request.POST.get('FORM') or None,
        topping_id=request.POST.get('TOPPING') or None,
        berry_id=request.POST.get('BERRIES') or None,
        decor_id=request.POST.get('DECOR') or None,
        inscription_text=(request.POST.get('WORDS') or '').strip(),
    )
    fake.recalc_subtotal(save=False)
    return JsonResponse({'price': float(fake.line_subtotal)})
