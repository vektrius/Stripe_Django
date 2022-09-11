from django.urls import path

from OrdersApp.views import get_product_checkout_view, ItemView, ItemCreateView, ItemListView, OrderView, \
    get_order_checkout_view, OrderListView, OrderCreateView


item_url_path = [
    path('buy/<int:item_id>/', get_product_checkout_view, name='buy_item'),
    path('items/<int:item_id>/', ItemView.as_view(), name='item'),
    path('item/create/', ItemCreateView.as_view(), name='create_item'),
    path('items/', ItemListView.as_view(), name='items_list'),
]

order_url_path = [
    path('orders/<int:order_id>/', OrderView.as_view(), name='order'),
    path('orders/buy/<int:order_id>/', get_order_checkout_view, name='buy_order'),
    path('orders/', OrderListView.as_view(), name='orders_list'),
    path('orders/create/', OrderCreateView.as_view(), name='create_order'),
]
urlpatterns = order_url_path + item_url_path
