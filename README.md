# BakeCake
ТЗ 
https://docs.google.com/document/d/1bQ9nWbLMhnNtJi45jaD1YreutSoQPpfq/edit?usp=sharing&ouid=118029468782242724621&rtpof=true&sd=true

Пояснения по orders/models.py

Order

Кто и когда оформил: customer, created_at, status.

Контакты и снапшот адреса: contact_name, phone, city/street/..., delivery_date, delivery_comment.

Юридика: consent_personal_data (галка согласия на ПД).

Маркетинг: utm_source/medium/campaign, promo_code.

Деньги: subtotal (сумма позиций), discount_total, delivery_fee, rush_fee (надбавка за доставку <24ч), total (итог).

OrderItem

Привязан к заказу (order).

Одиночные выборы: levels, shape, topping — FK на Option с ограничением по category__slug (нельзя выбрать «ягоду» в поле «форма»).

Надпись: inscription_text + inscription_price.

Мультивыбор: berries и decors — M2M через OrderItemBerry/OrderItemDecor, чтобы зафиксировать цену на момент покупки.

Деньги по позиции: base_price, line_subtotal.

OrderItemBerry / OrderItemDecor (through-модели)

Связка item + option и поле price_at_purchase.
Это и есть ценовой снапшот для каждой ягоды/декора.