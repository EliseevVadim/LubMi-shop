from django.conf import settings
from lms.models import Product


class Favorites:
    def __init__(self, request):
        self.session = request.session
        favorites = self.session.get(settings.FAVORITES_SESSION_ID)
        if not favorites:
            favorites = self.session[settings.FAVORITES_SESSION_ID] = set()
        self._favorites = favorites

    def clear(self):
        del self.session[settings.FAVORITES_SESSION_ID]
        self.save()

    def add_item(self, prod_id: str):
        if prod_id not in self._favorites:
            self._favorites.add(prod_id)
        self.save()

    def remove_item(self, prod_id: str):
        if prod_id in self._favorites:
            self._favorites.discard(prod_id)
            self.save()

    def __iter__(self):
        products = Product.objects.filter(article__in=self._favorites)
        for product in products:
            yield product

    def __len__(self):
        return len(self._favorites)

    def save(self):
        self.session.modified = True
