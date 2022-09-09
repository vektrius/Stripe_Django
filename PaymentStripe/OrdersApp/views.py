import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import stripe
from django.urls import reverse
from django.views.generic import DetailView, CreateView, ListView

from OrdersApp.models import Item

# Create your views here.


stripe.api_key = os.getenv("STRIPE_KEY_BACKEND")


def GetSessionIdView(request, item_id: int):
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


class ItemView(DetailView):
    model = Item
    pk_url_kwarg = 'item_id'
    context_object_name = 'item'
    template_name = 'item_buy.html'


class ItemCreateView(CreateView):
    model = Item
    fields = '__all__'
    template_name = 'item_create.html'
    success_url = '/create'


class ItemListView(ListView):
    model = Item
    template_name = 'items.html'
    context_object_name = 'items'
