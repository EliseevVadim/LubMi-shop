from django.conf import settings


class CustomerInfo:
    def __init__(self, request):
        self.session = request.session
        favorites = self.session.get(settings.CUSTOMER_INFO_SESSION_ID)
        if not favorites:
            favorites = self.session[settings.CUSTOMER_INFO_SESSION_ID] = list()
        self._favorites = favorites

    def clear(self):
        del self.session[settings.CUSTOMER_INFO_SESSION_ID]
        self.save()

    def add_item(self, prod_id: str):
        if prod_id not in self._favorites:
            self._favorites.append(prod_id)
            self.save()

    def remove_item(self, prod_id: str):
        if prod_id in self._favorites:
            self._favorites.remove(prod_id)
            self.save()

    @property
    def favorites(self):
        return list(self._favorites)

    def __len__(self):
        return len(self._favorites)

    def __contains__(self, item: str):
        return item in self._favorites

    def save(self):
        self.session.modified = True
