import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import stripe
from django.urls import reverse
from django.views.generic import DetailView, CreateView, ListView

from OrdersApp.models import Item, Order

# Create your views here.


stripe.api_key = os.getenv("STRIPE_KEY_BACKEND")


def GetProductCheckOutView(request, item_id: int):
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


def GetOrderCheckOutView(request, order_id: int):
    ''' Get session id for the order '''

    order = Order.objects.prefetch_related('items').get(pk=order_id)

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
        } for item in order.items.all()],

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
