from django.urls import path
from .views import *

app_name = 'lms'

urlpatterns = [
    # -- main --
    path('', IndexView.as_view(), name='index'),
    path('catalogue/', CatalogueView.as_view(), name='catalogue'),
    path('perfumery/', PerfumeryView.as_view(), name='perfumery'),
    path('delivery/', DeliveryView.as_view(), name='delivery'),
    path('care/', CareView.as_view(), name='care'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('about/', AboutCompanyView.as_view(), name='about'),
    # -- backstage --
    path('product/<slug:slug>/', ProductView.as_view(), name='product_details'),
    path('shopping-cart/', SCartView.as_view(), name='scart'),
    path('favorite-list/', FavoritesView.as_view(), name='favorites'),
    path('c6t-scart/', C6tScartView.as_view(), name='c6t_scart'),
    path('c6t-form/', C6tFormView.as_view(), name='c6t_form'),
]
