from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views import View
from customerinfo.customerinfo import CustomerInfo
from .models import *
from .forms import ShortCustomerInfoForm
from decimal import Decimal


# -------------------------------------------------------------------------
# -- Main views --

class IndexView(View):
    page_size = 10
    default_order = 'novelties-first'
    ordering = {
        default_order: ("Порядок: по умолчанию", lambda q: q.order_by('-published_at')),
        'price-asc': ("Цена: по возрастанию", lambda q: q.order_by('actual_price')),
        'price-dsc': ("Цена: по убыванию", lambda q: q.order_by('-actual_price')),
        'title-asc': ("Название: А-Я", lambda q: q.order_by('title')),
        'title-dsc': ("Название: Я-А", lambda q: q.order_by('-title')),
    }

    @staticmethod
    def get(request, *_, **__):
        page = request.GET.get('page')
        order = request.GET.get('order')
        order = order if order in IndexView.ordering else IndexView.default_order
        products = IndexView.ordering[order][1](Product.published.all())
        bestsellers = Product.bestsellers.all()
        pd_pgn = Paginator(products, IndexView.page_size)
        bs_pgn = Paginator(bestsellers, IndexView.page_size)
        favorites = CustomerInfo(request).favorites

        if not page:
            return render(request, 'lms/index.html', {
                'page_title': "Главная",
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


class CatalogueView(ListView):
    queryset = Product.published.all()
    context_object_name = 'products'
    paginate_by = 3
    template_name = 'lms/under_work.html'


class PerfumeryView(ListView):
    queryset = Product.published.all()
    context_object_name = 'products'
    paginate_by = 3
    template_name = 'lms/under_work.html'


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
    template_name = 'lms/pcard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favorites = CustomerInfo(self.request).favorites
        return context | {
            'favorites': favorites,
        }


class SCartView(View):
    @staticmethod
    def get(request, *_, **__):
        info = CustomerInfo(request)
        sct = info.scart
        records = []
        price = Decimal(0)
        for ppk, sizes in sct.items():
            product = Product.objects.get(pk=ppk)
            for sz, quantity in sizes.items():
                size = product.sizes.get(size=sz)
                records += [{
                    'product': product,
                    'size': size,
                    'quantity': quantity
                }]
                price += quantity * product.actual_price.amount
        return render(request, 'lms/scart.html', {
            'scart': records,
            'price': price
        })
