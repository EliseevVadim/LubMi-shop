from django.conf import settings
from lms.models import AvailableSize, Product
from decimal import Decimal


class SCart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.SCART_SESSION_ID)
        if not cart:
            cart = self.session[settings.SCART_SESSION_ID] = {}
        self._cart = cart

    def clear(self):
        del self.session[settings.SCART_SESSION_ID]
        self.save()

    def add_item(self, size: AvailableSize, quantity: int = 1, accumulate: bool = True):
        prod_id: str = str(size.product.article)
        if prod_id not in self._cart:
            self._cart[prod_id] = {'size': size.size, 'price': size.product.actual_price, 'quantity': 0}
        if accumulate:
            self._cart[prod_id]['quantity'] += quantity
        else:
            self._cart[prod_id]['quantity'] = quantity
        self.save()

    def remove_item(self, prod_id: str):
        if prod_id in self._cart:
            del self._cart[prod_id]
            self.save()

    def get_total_price(self):
        return sum(item['quantity'] * Decimal(item['price']) for item in self._cart.values())

    def __iter__(self):
        product_ids = self._cart.keys()
        products = Product.objects.filter(article__in=product_ids)
        cart = self._cart.copy()
        for product in products:
            cart[str(product.article)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self._cart.values())

    def save(self):
        self.session.modified = True
