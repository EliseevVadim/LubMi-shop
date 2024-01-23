from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views import View
from .models import *
from customerinfo.customerinfo import CustomerInfo


class IndexView(View):
    page_size = 10
    default_order = 'published'
    ordering = {
        default_order: lambda q: q.order_by('published_at'),
        'title': lambda q: q.order_by('title'),
        'price': lambda q: q.order_by('actual_price'),
        'sales': lambda q: q.order_by('sales_quantity'),
    }

    @staticmethod
    def get(request, *_, **__):
        page = request.GET.get('page')
        order = request.GET.get('order')
        order = order if order in IndexView.ordering else IndexView.default_order
        products = IndexView.ordering[order](Product.published.all())
        bestsellers = Product.bestsellers.all()
        pd_pgn = Paginator(products, IndexView.page_size)
        bs_pgn = Paginator(bestsellers, IndexView.page_size)
        favorites = CustomerInfo(request).favorites

        if not page:
            return render(request, 'lms/index.html', {
                'page_title': "LubMi - Главная",
                'products': pd_pgn.page(1),
                'bestsellers': bs_pgn.page(1),
                'product_pages': pd_pgn.num_pages,
                'bestseller_pages': bs_pgn.num_pages,
                'order': order,
                'favorites': favorites,
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


class ProductView(ListView):
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


class AboutCompanyView(ListView):
    queryset = Product.published.all()
    context_object_name = 'products'
    paginate_by = 3
    template_name = 'lms/under_work.html'
