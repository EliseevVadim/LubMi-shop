from django.conf import settings
from decimal import Decimal
from rest_framework.response import Response
from lms.models import Product, AvailableSize, Parameter
import time


def api_response(func):
    def tune_dict(result, flag: bool = True):
        if 'success' not in result:
            result['success'] = flag
        return result

    def deco(*args, **kwargs):
        result = func(*args, **kwargs)
        return Response(tune_dict(result)) if type(result) is dict \
            else Response({'success': False, 'why': result}) if type(result) is str \
            else Response({'success': result[0], 'why': result[1]}) if type(result) is tuple and len(result) == 2 and type(result[0]) is bool and type(result[1]) is str \
            else result
    return deco


def on_except_return(value):
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except:
                return value
        return wrapper
    return decorator


def sleep_and_retry_on_except(timeout, result_on_fail, retry=5, validator=lambda _: True):
    def decorator(function):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retry:
                try:
                    if not validator(value := function(*args, **kwargs)):
                        raise ValueError(value)
                except:
                    print(f'Sleeping for {timeout} seconds')
                    time.sleep(timeout)
                    attempts += 1
                else:
                    return value
            return result_on_fail
        return wrapper
    return decorator


def sleep_after(delay=settings.SLEEP_AFTER):
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                value = function(*args, **kwargs)
            finally:
                time.sleep(delay)
            return value
        return wrapper
    return decorator


def with_scart_from_request(scart_field_name):
    def decorator(func):
        def proxy(request, *args, **kwargs):
            data = request.data
            records = []
            errors = []
            actual_price = Decimal(0)
            old_price = Decimal(0)
            weight = 0

            def err(typ, text, reason):
                errors.append({
                    "error-type": typ,
                    "error-text": text,
                    "error-reason": reason,
                })

            if scart_field_name in data:
                try:
                    for sd in data[scart_field_name]:
                        ppk, size_id, quantity = str(sd['ppk']), int(sd['size_id']), abs(int(sd['quantity']))
                        try:
                            product: Product = Product.published.get(pk=ppk)
                            size: AvailableSize = product.sizes.get(pk=size_id)
                        except (Product.DoesNotExist, AvailableSize.DoesNotExist):
                            err("item-does-not-exist", "Товар или размер не найдены", {"ppk": ppk, "size_id": size_id})
                        else:
                            old_price += quantity * (product.old_price.amount if product.old_price else product.actual_price.amount)
                            actual_price += quantity * product.actual_price.amount
                            weight += quantity * product.weight
                            records += [{
                                'product': product,
                                'size': size,
                                'quantity': quantity
                            }]
                            if size.quantity < quantity:
                                err("insufficient-product-quantity", "В наличии нет нужного количества товара", {"ppk": ppk, "size_id": size_id, "required": quantity, "available": size.quantity})
                except (TypeError, KeyError):
                    return Parameter.value_of('message_data_sending_error', 'Произошла ошибка при отправке данных, мы работаем над этим...')
                except ValueError:
                    return Parameter.value_of('message_data_retrieving_error', 'Произошла ошибка при извлечении данных, мы работаем над этим...')
            return func(request,
                        *args,
                        **kwargs,
                        scart={
                            'records': records,
                            'price': actual_price,
                            'old_price': old_price,
                            'weight': weight},
                        errors=errors)
        return proxy
    return decorator
