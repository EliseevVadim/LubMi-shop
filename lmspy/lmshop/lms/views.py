import decimal

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views import View
from django.template.defaultfilters import floatformat
from customerinfo.customerinfo import CustomerInfo, with_actual_scart_records_and_price
from .models import *
from .forms import ShortCustomerInfoForm, CheckoutForm


# -------------------------------------------------------------------------
# -- Main views --

class IndexView(View):
    page_size = 10
    default_order = 'novelties-first'
    ordering = {
        default_order: ("Порядок: по умолчанию", lambda q: q.order_by('-published_at')),  # TODO -- move labels to parameters! --
        'price-asc': ("Цена: по возрастанию", lambda q: q.order_by('actual_price')),
        'price-dsc': ("Цена: по убыванию", lambda q: q.order_by('-actual_price')),
        'title-asc': ("Название: А-Я", lambda q: q.order_by('title')),
        'title-dsc': ("Название: Я-А", lambda q: q.order_by('-title')),
    }

    @property
    def template_name(self):
        return 'lms/index.html'

    def get(self, request, *_, **__):
        page = request.GET.get('page')
        order = request.GET.get('order')
        order = order if order in IndexView.ordering else IndexView.default_order
        products = IndexView.ordering[order][1](Product.published.all())
        bestsellers = Product.bestsellers.all()
        pd_pgn = Paginator(products, IndexView.page_size)
        bs_pgn = Paginator(bestsellers, IndexView.page_size)
        favorites = CustomerInfo(request).favorites

        if not page:
            return render(request, self.template_name, {
                'page_title': Parameter.value_of("title_main_page", "Главная"),
                'products': pd_pgn.page(1),
                'bestsellers': bs_pgn.page(1),
                'product_pages': pd_pgn.num_pages,
                'bestseller_pages': bs_pgn.num_pages,
                'order': order,
                'order_variants': {order_value: order_item[0] for order_value, order_item in IndexView.ordering.items()},
                'favorites': favorites,
                'scui_form': ShortCustomerInfoForm(),
            })

        match request.GET.get('kind'):
            case 'bs':
                pgn = bs_pgn
            case _:
                pgn = pd_pgn

        try:
            return render(request, 'lms/plist.html', {
                'products': pgn.page(page),
                'favorites': favorites,
            })
        except PageNotAnInteger:
            return HttpResponse('')
        except EmptyPage:
            return HttpResponse('')
        except ValueError:
            return HttpResponse('')


class CatalogueView(IndexView):
    @property
    def template_name(self):
        return 'lms/catalogue.html'


class PerfumeryView(View):
    @staticmethod
    def get(request, *_, **__):
        return render(request, 'lms/perfumery.html', {
            'page_title': Parameter.value_of("title_perfumery", "Парфюмерия"),
        })


class DeliveryView(ListView):
    queryset = Product.published.all()
    context_object_name = 'products'
    paginate_by = 3
    template_name = 'lms/under_work.html'


class CareView(ListView):
    queryset = Product.published.all()
    context_object_name = 'products'
    paginate_by = 3
    template_name = 'lms/under_work.html'


class ContactsView(ListView):
    queryset = Product.published.all()
    context_object_name = 'products'
    paginate_by = 3
    template_name = 'lms/under_work.html'


class AboutCompanyView(View):
    @staticmethod
    def get(request, *_, **__):
        return render(request, 'lms/under_work.html', {
            'page_title': "Работа в процессе",
        })


# -------------------------------------------------------------------------
# -- Backstage views --

class ProductView(DetailView):
    model = Product
    queryset = Product.published.all()
    template_name = 'lms/pcard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favorites = CustomerInfo(self.request).favorites
        return context | {
            'favorites': favorites,
        }


class SCartView(View):
    @staticmethod
    @with_actual_scart_records_and_price
    def get(request, scart, *_, **__):
        return render(request, 'lms/scart.html', scart)


class FavoritesView(View):
    @staticmethod
    def get(request, *_, **__):
        return render(request, 'lms/favorites.html', {
            'products': Product.published.filter(pk__in=CustomerInfo(request).favorites),
        })


class C6tFormView(View):
    @staticmethod
    def get(request, *_, **__):
        return render(request, 'lms/c6t-form.html', {
            'c6t_form': CheckoutForm(),
        })


class C6tScartView(View):
    @staticmethod
    @with_actual_scart_records_and_price
    def get(request, scart, *_, **__):
        return render(request, 'lms/c6t-scart.html', scart)


class C6tInfoView(View):
    @staticmethod
    @with_actual_scart_records_and_price
    def get(request, kind, data, scart, *_, **__):
        match kind:
            case 'delivery':
                dv_cost = decimal.Decimal(459.70 if data == "sd" else 512.00)  # TODO !!!
                dv_days = decimal.Decimal(3 if data == "sd" else 5)  # TODO !!!
                return render(request, 'lms/c6t-d6y.html', {
                    "cost":  floatformat(dv_cost, 2),
                    "days": floatformat(dv_days),
                })
            case 'cities':
                return render(request, 'lms/c6t-city-list.html', {
                    "cities": ["СДЭК-Москва", "СДЭК-Донецк", "СДЭК-Луганск"] if data == 'sd' else ["ПР-Москва", "ПР-Донецк", "ПР-Луганск"],
                })
            case 'summary':
                dv_cost = decimal.Decimal(719.50 if data == 'sd' else 820.10)  # TODO !!!
                city = request.GET.get('city')
                return render(request, 'lms/c6t-summary.html', {
                    "items": {
                        "Сумма": f'{floatformat(scart["price"], 2)} {Parameter.value_of("label_currency")}',
                        "Доставка": f'{"СДЭК" if data == "sd" else "Почта России"}, {floatformat(dv_cost, 2)} {Parameter.value_of("label_currency")}',
                        "Назначение": f'{city if city else "г. Москва, Россия"}',
                        "Итоговая сумма": f'{floatformat(scart["price"] + dv_cost, 2)} {Parameter.value_of("label_currency")}',
                    }
                })
            case _: return render(request, 'lms/c6t-summary.html', {
                "items": {
                    "Ошибка": "Запрошен неизвестный тип данных"
                }
            })
