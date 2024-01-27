from django.conf import settings
from hashlib import sha256

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

    @staticmethod
    def _hash(s1, s2):
        h1 = int(sha256(s1.encode()).hexdigest(), 16)
        h2 = int(sha256(s2.encode()).hexdigest(), 16)
        return hex(h1 ^ h2 if h1 != h2 else h2)

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

    def add_to_scart(self, ppk, size, quantity, dry_run=False):    # -- accumulative operation, negative quantity decreases total quantity in SCart --
        sct = self._get_or_create_scart()
        print(sct)
        key = CustomerInfo._hash(ppk, size)
        rec = sct.setdefault(key, {'ppk': ppk, 'size': size, 'quantity': 0})
        if dry_run:
            rec = rec.copy()
        try:
            new_quantity = rec['quantity'] = max(rec['quantity'] + quantity, 0)
            if new_quantity == 0 and not dry_run:
                del sct[key]
            return new_quantity
        finally:
            if not dry_run:
                self.save()

    def clear_scart(self):
        sct = self._get_or_create_scart()
        sct.clear()
        self.save()

    @property
    def scart(self):
        sct = self._get_or_create_scart()
        result = dict()
        for rec in sct.values():
            result.setdefault(rec['ppk'], dict())[rec['size']] = rec['quantity']
        return result

    @property
    def favorites(self):
        return set(self._get_or_create_favorites())

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
        return self._get_or_create_item("address", lambda: {
            "country": "",
            "city": "",
            "address": ""
        })

    @address.setter
    def address(self, value):
        self._set_item("address", value)

    @address.deleter
    def address(self):
        self._delete_item("address")

    def save(self):
        self.session.modified = True
