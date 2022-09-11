import os
import time
from decimal import Decimal

import requests
from django.http import JsonResponse
import stripe
from django.views.generic import DetailView, CreateView, ListView

from OrdersApp.models import Item, Order

stripe.api_key = os.getenv("STRIPE_KEY_BACKEND")


def _сonvertation(item: Item, exchange_rates: dict) -> Decimal:
    ''' Convertation item currency  to need currency '''

    converted_price = float(item.price) / exchange_rates[item.currency]
    return Decimal(converted_price).quantize(Decimal("1.00"))


def get_product_checkout_view(request, item_id: int) -> JsonResponse:
    ''' Get session id for the item '''

    item = Item.objects.get(pk=item_id)
    print(item)
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount_decimal': item.price * 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://url.com',
        cancel_url='https://url.com',
    )
    return JsonResponse({"session_id": session.id})


def get_order_checkout_view(request, order_id: int) -> JsonResponse:
    ''' Get session id for the order '''

    order = Order.objects.prefetch_related('items', 'discounts', 'taxes').get(pk=order_id)

    time1 = time.time()
    session = stripe.checkout.Session.create(
        line_items=_get_line_items_for_order(order),
        discounts=_get_coupon_for_order(order),
        mode='payment',
        success_url='https://url.com',
        cancel_url='https://url.com',
    )
    print(time.time() - time1)
    return JsonResponse({"session_id": session.id})


def _get_line_items_for_order(order: Order) -> list[dict]:
    ''' Get line items for order '''

    exchange_rates = requests.get(f"https://api.exchangerate-api.com/v4/latest/{order.currency}").json()['rates']

    return [{
        'price_data': {
            'currency': order.currency,
            'product_data': {
                'name': item.name,
            },
            'unit_amount_decimal': _сonvertation(item, exchange_rates) * 100,
        },
        'quantity': 1,
        'tax_rates': _get_tax_rates_for_order(order)
    } for item in order.items.all()]


def _get_tax_rates_for_order(order: Order) -> list[dict]:
    ''' Get tax rates for order '''

    return [stripe.TaxRate.create(display_name=tax.name, inclusive=tax.inclusive, percentage=tax.percentage).id
            for tax in order.taxes.all()]


def _get_coupon_for_order(order: Order) -> list[dict]:
    ''' Get coupon for order '''

    return [{
        'coupon': stripe.Coupon.create(
            percent_off=coupon.percent_off,
            duration=coupon.duration,
            duration_in_months=coupon.duration_in_months,
        ).id} for coupon in order.discounts.all()]


class ItemView(DetailView):
    model = Item
    pk_url_kwarg = 'item_id'
    context_object_name = 'item'
    template_name = 'item/item_buy.html'


class ItemCreateView(CreateView):
    model = Item
    fields = '__all__'
    template_name = 'item/item_create.html'
    success_url = '/'


class ItemListView(ListView):
    model = Item
    template_name = 'item/items.html'
    context_object_name = 'items'


class OrderView(DetailView):
    model = Order
    pk_url_kwarg = 'order_id'
    context_object_name = 'order'
    template_name = 'order/order_buy.html'

    def get_object(self, queryset=None):
        return Order.objects.prefetch_related("items").get(id=self.kwargs[self.pk_url_kwarg])


class OrderCreateView(CreateView):
    model = Order
    fields = '__all__'
    template_name = 'order/order_create.html'
    success_url = '/'


class OrderListView(ListView):
    model = Order
    template_name = 'order/orders.html'
    context_object_name = 'orders'
