"""PaymentStripe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path

from OrdersApp.views import get_product_checkout_view, ItemView, ItemCreateView, ItemListView, OrderCreateView, OrderView, \
    get_order_checkout_view, OrderListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buy/<int:item_id>/', get_product_checkout_view, name='buy_item'),
    path('items/<int:item_id>/', ItemView.as_view(), name='item'),
    path('orders/<int:order_id>/', OrderView.as_view(), name='order'),
    path('orders/buy/<int:order_id>/', get_order_checkout_view, name='buy_order'),
    path('item/create/', ItemCreateView.as_view(), name='create_item'),
    path('items/', ItemListView.as_view(), name='items_list'),
    path('orders/', OrderListView.as_view(), name='orders_list'),
    path('orders/create/', OrderCreateView.as_view(),name='create_order'),
    path('', lambda request: render(request, 'main.html', {}), name='main')
]
