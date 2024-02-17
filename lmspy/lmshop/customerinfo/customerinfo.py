from _decimal import Decimal
from django.conf import settings
from hashlib import sha256
from lms.models import Product, AvailableSize
from lms.utils import find_nearest_city, earth_dist
from functools import lru_cache


class CustomerInfo:
    def __init__(self, request):
        self.session = request.session
        info = self.session.get(settings.CUSTOMER_INFO_SESSION_ID)
        if not info:
            info = self.session[settings.CUSTOMER_INFO_SESSION_ID] = dict()
        self._info = info

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CUSTOMER_INFO_SESSION_ID]
        self.save()

    # -------------------------------------------------------------------------
    # -- Privates --

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
    @lru_cache
    def _hash(s1, s2):
        h1 = int(sha256(s1.encode()).hexdigest(), 16)
        h2 = int(sha256(s2.encode()).hexdigest(), 16)
        return hex(h1 ^ h2 if h1 != h2 else h2)

    # -------------------------------------------------------------------------
    # -- Favorites --

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

    # -------------------------------------------------------------------------
    # -- Shopping cart --

    def add_to_scart(self, ppk, size, quantity, dry_run=False):    # -- accumulative operation, negative quantity decreases total quantity in SCart --
        sct = self._get_or_create_scart()
        key = CustomerInfo._hash(ppk, size)
        sc_rec = sct.setdefault(key, {'ppk': ppk, 'size': size, 'quantity': 0})
        if dry_run:
            sc_rec = sc_rec.copy()
        try:
            new_quantity = sc_rec['quantity'] = max(sc_rec['quantity'] + quantity, 0)
            if new_quantity == 0 and not dry_run:
                del sct[key]
            return new_quantity
        finally:
            if not dry_run:
                self.save()

    def remove_from_scart(self, ppk, size, dry_run=False):
        sct = self._get_or_create_scart()
        key = CustomerInfo._hash(ppk, size)
        if dry_run:
            try:
                return sct[key].copy()
            except KeyError:
                return None
        else:
            try:
                return sct.pop(key, None)
            finally:
                self.save()

    def clear_scart(self):
        sct = self._get_or_create_scart()
        sct.clear()
        self.save()

    @property
    def scart(self):
        sct = self._get_or_create_scart()
        result = dict()
        for sc_rec in sct.values():
            result.setdefault(sc_rec['ppk'], dict())[sc_rec['size']] = sc_rec['quantity']
        return result

    # -------------------------------------------------------------------------
    # -- Name --

    @property
    def name(self):
        return self._get_or_create_item("name", str)

    @name.setter
    def name(self, value):
        self._set_item("name", value)

    @name.deleter
    def name(self):
        self._delete_item("name")

    # -------------------------------------------------------------------------
    # -- Phone --

    @property
    def phone(self):
        return self._get_or_create_item("phone", str)

    @phone.setter
    def phone(self, value):
        self._set_item("phone", value)

    @phone.deleter
    def phone(self):
        self._delete_item("phone")

    # -------------------------------------------------------------------------
    # -- Email --

    @property
    def email(self):
        return self._get_or_create_item("email", str)

    @email.setter
    def email(self, value):
        self._set_item("email", value)

    @email.deleter
    def email(self):
        self._delete_item("email")

    # -------------------------------------------------------------------------
    # -- Address --

    @property
    def address(self):
        return self._get_or_create_item("address", lambda: {
            "country": "",
            "city_uuid": "",
            "city": "",
            "street": "",
            "building": "",
            "entrance": "",
            "floor": "",
            "apartment": "",
            "fullname": "",
        })

    @address.setter
    def address(self, value):
        self._set_item("address", value)

    @address.deleter
    def address(self):
        self._delete_item("address")

    # -------------------------------------------------------------------------
    # -- Payment Id --

    @property
    def payment_id(self):
        return self._get_or_create_item("payment_id", str)

    @payment_id.setter
    def payment_id(self, value):
        self._set_item("payment_id", value)

    @payment_id.deleter
    def payment_id(self):
        self._delete_item("payment_id")

    # -------------------------------------------------------------------------
    # -- Location --

    @property
    def location(self):
        return self._get_or_create_item("location", lambda: {
            "latitude": None,
            "longitude": None,
            "accuracy": None,
        })

    @location.setter
    def location(self, value):
        def update_city(lat, lng):
            try:
                addr = self.address
                if not addr["city_uuid"] and not addr["city"]:
                    city = find_nearest_city(lat, lng)
                    if city:
                        addr["city_uuid"], addr["city"] = str(city.city_uuid), city.city_full
                        self.address = addr
            except (KeyError, ValueError, TypeError):
                pass
        try:
            n_lat = value['latitude']
            n_lng = value['longitude']
        except KeyError:
            return
        else:
            try:
                n_lat = float(n_lat)
                n_lng = float(n_lng)
            except (TypeError, ValueError):
                return
            else:
                current = self.location
                try:
                    c_lat = current['latitude']
                    c_lng = current['longitude']
                except KeyError:
                    update_city(n_lat, n_lng)
                else:
                    try:
                        c_lat = float(c_lat)
                        c_lng = float(c_lng)
                    except (TypeError, ValueError):
                        update_city(n_lat, n_lng)
                    else:
                        if earth_dist(c_lat, c_lng, n_lat, n_lng) > 1000.0:
                            update_city(n_lat, n_lng)
        self._set_item("location", value)

    @location.deleter
    def location(self):
        self._delete_item("location")


def with_actual_scart_records_and_price(func):
    def deco(request, *args, **kwargs):
        records = []
        price = Decimal(0)
        weight = 0
        for ppk, sizes in CustomerInfo(request).scart.items():
            try:
                product = Product.published.get(pk=ppk)
            except Product.DoesNotExist:
                continue
            for size_str, quantity in sizes.items():
                try:
                    size = product.sizes.get(size=size_str)
                except AvailableSize.DoesNotExist:
                    pass
                else:
                    records += [{
                        'product': product,
                        'size': size,
                        'quantity': quantity
                    }]
                    price += quantity * product.actual_price.amount
                    weight += quantity * product.weight
        return func(request, *args, **kwargs, scart={'records': records, 'price': price, 'weight': weight})
    return deco
