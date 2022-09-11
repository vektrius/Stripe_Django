import os
from decimal import Decimal, getcontext
from typing import Literal

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import stripe
from django.urls import reverse
from django.views.generic import DetailView, CreateView, ListView

from OrdersApp.models import Item, Order

# Create your views here.


stripe.api_key = os.getenv("STRIPE_KEY_BACKEND")


def сonvertation(item: Item, currency: Literal['USD', 'RUB']) -> Decimal:
    ''' Convertation item currency  to need currency '''

    item_currency = item.currency.upper()
    exchange_rates = requests.get(f"https://api.exchangerate-api.com/v4/latest/{item_currency}").json()['rates']
    converted_price = float(item.price) * exchange_rates[currency]
    return Decimal(converted_price).quantize(Decimal("1.00"))


def get_product_checkout_view(request, item_id: int):
    ''' Get session id for the item '''

    item = Item.objects.get(pk=item_id)
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
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


def get_order_checkout_view(request, order_id: int):
    ''' Get session id for the order '''

    order = Order.objects.prefetch_related('items', 'discounts').get(pk=order_id)
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': order.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount_decimal': сonvertation(item, order.currency) * 100,
            },
            'quantity': 1,
        } for item in order.items.all()],
        discounts=[{
            'coupon': stripe.Coupon.create(
                percent_off=coupon.percent_off,
                duration=coupon.duration,
                duration_in_months=coupon.duration_in_months,
            ).id} for coupon in order.discounts.all()],

        mode='payment',
        success_url='https://url.com',
        cancel_url='https://url.com',
    )

    return JsonResponse({"session_id": session.id})


class ItemView(DetailView):
    model = Item
    pk_url_kwarg = 'item_id'
    context_object_name = 'item'
    template_name = 'item_buy.html'


class ItemCreateView(CreateView):
    model = Item
    fields = '__all__'
    template_name = 'item_create.html'
    success_url = '/'


class ItemListView(ListView):
    model = Item
    template_name = 'items.html'
    context_object_name = 'items'


class OrderView(DetailView):
    model = Order
    pk_url_kwarg = 'order_id'
    context_object_name = 'order'
    template_name = 'order_buy.html'

    def get_object(self, queryset=None):
        return Order.objects.prefetch_related("items").get(id=self.kwargs[self.pk_url_kwarg])


class OrderCreateView(CreateView):
    model = Order
    fields = '__all__'
    template_name = 'order_create.html'
    success_url = '/'


class OrderListView(ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'
