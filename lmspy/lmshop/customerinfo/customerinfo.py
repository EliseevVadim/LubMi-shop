from django.conf import settings


class CustomerInfo:
    def __init__(self, request):
        self.session = request.session
        info = self.session.get(settings.CUSTOMER_INFO_SESSION_ID)
        if not info:
            info = self.session[settings.CUSTOMER_INFO_SESSION_ID] = dict()
        self._info = info

    def clear(self):
        del self.session[settings.CUSTOMER_INFO_SESSION_ID]
        self.save()

    def _get_or_create_item(self, key, builder, save=False):
        try:
            result = self._info[key]
        except KeyError:
            result = self._info[key] = builder()
            if save:
                self.save()
        return result

    def _set_item(self, key, value, save=True):
        self._info[key] = value
        if save:
            self.save()

    def _delete_item(self, key, save=True):
        try:
            del self._info[key]
        except KeyError:
            return 
        if save:
            self.save()

    def _get_or_create_favorites(self):
        return self._get_or_create_item("favorites", list)

    def _get_or_create_scart(self):
        return self._get_or_create_item("scart", dict)  # { ppk: order_info }

    def add_favorite(self, ppk):
        favorites = self._get_or_create_favorites()
        if ppk not in favorites:
            favorites.append(ppk)
            self.save()

    def remove_favorite(self, ppk: str):
        favorites = self._get_or_create_favorites()
        if ppk in favorites:
            favorites.remove(ppk)
            self.save()

    @property
    def favorites(self):
        return set(self._get_or_create_favorites())

    @property
    def scart(self):
        return set(self._get_or_create_scart())

    @property
    def name(self):
        return self._get_or_create_item("name", str)

    @name.setter
    def name(self, value):
        self._set_item("name", value)

    @name.deleter
    def name(self):
        self._delete_item("name")

    @property
    def phone(self):
        return self._get_or_create_item("phone", str)

    @phone.setter
    def phone(self, value):
        self._set_item("phone", value)

    @phone.deleter
    def phone(self):
        self._delete_item("phone")

    @property
    def email(self):
        return self._get_or_create_item("email", str)

    @email.setter
    def email(self, value):
        self._set_item("email", value)

    @email.deleter
    def email(self):
        self._delete_item("email")

    @property
    def address(self):
        return self._get_or_create_item("address",
                                        lambda: {
                                            "Страна": "",
                                            "Город": "",
                                            "Адрес": ""
                                        })

    @address.setter
    def address(self, value):
        self._set_item("address", value)

    @address.deleter
    def address(self):
        self._delete_item("address")

    def save(self):
        self.session.modified = True
