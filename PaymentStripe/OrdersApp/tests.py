from django.test import TestCase
from django.urls import reverse

from OrdersApp.models import Item, Order


# Create your tests here.


class ViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.item = Item.objects.create(name='Item', description="Dedas", price=100, currency="USD")
        self.order = Order.objects.create(currency="USD")
        self.order.items.add(self.item)

    def test_views_response(self):
        item_url = (
            reverse('items_list'), reverse('item', kwargs={'item_id': self.item.pk}),
            reverse('create_item'), reverse('buy_item', kwargs={'item_id': self.item.pk})
        )

        order_url = (
            reverse('orders_list'),reverse('order', kwargs={'order_id': self.order.pk}),
            reverse('create_order'),reverse('buy_order', kwargs={'order_id': self.order.pk}),
        )


        tested_url = (reverse('main'),) + item_url + order_url

        for url in tested_url:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

