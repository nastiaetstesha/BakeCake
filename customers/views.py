from django.shortcuts import render
from django.views import View
from orders.models import Order


class ClientProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "lk.html", {"client_orders": []})
        
        # Получаем заказы пользователя с предзагрузкой связанных данных
        orders = Order.objects.filter(customer__user=request.user).prefetch_related(
            'items',
            'items__levels',
            'items__shape', 
            'items__topping',
            'items__berry_links',
            'items__berry_links__option',
            'items__decor_links',
            'items__decor_links__option',
        ).order_by('-created_at')
        
        client_orders = []

        for order in orders:
            order_data = {
                "order_id": order.id,
                "status": order.get_status_display(),
                "status_code": order.status,
                "total": order.total,
                "delivery_date": order.delivery_date,
                "created_at": order.created_at,
                "items": []
            }
            
            for item in order.items.all():
                berries_with_prices = []
                for berry_link in item.berry_links.all():
                    berries_with_prices.append({
                        'title': berry_link.option.title,
                        'price': berry_link.price_at_purchase
                    })
                
                decors_with_prices = []
                for decor_link in item.decor_links.all():
                    decors_with_prices.append({
                        'title': decor_link.option.title,
                        'price': decor_link.price_at_purchase
                    })
                
                item_data = {
                    "base_price": item.base_price,
                    "line_subtotal": item.line_subtotal,
                    "levels": item.levels.title if item.levels else "Не выбрано",
                    "shape": item.shape.title if item.shape else "Не выбрано",
                    "topping": item.topping.title if item.topping else "Не выбрано",
                    "inscription": item.inscription_text if item.inscription_text else "Без надписи",
                    "inscription_price": item.inscription_price,
                    "berries": berries_with_prices,
                    "decors": decors_with_prices
                }
                
                order_data["items"].append(item_data)
            
            client_orders.append(order_data)

        context = {
            "client_orders": client_orders,
        }

        return render(request, "lk.html", context)
