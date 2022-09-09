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

from OrdersApp.views import GetSessionIdView, ItemView, ItemCreateView, ItemListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buy/<int:item_id>/', GetSessionIdView, name='getsession'),
    path('item/<int:item_id>/', ItemView.as_view(), name='item'),
    path('create/', ItemCreateView.as_view(), name='create_item'),
    path('items/', ItemListView.as_view(), name='items_list'),
    path('', lambda request: render(request, 'main.html', {}), name='main')
]