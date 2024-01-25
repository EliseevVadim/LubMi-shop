from django.urls import path
from .views import *

app_name = 'lms'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalogue/', CatalogueView.as_view(), name='catalogue'),
    path('product/<slug:slug>/', ProductView.as_view(), name='product_details'),
    path('perfumery/', PerfumeryView.as_view(), name='perfumery'),
    path('delivery/', ProductView.as_view(), name='delivery'),
    path('care/', CareView.as_view(), name='care'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('about/', AboutCompanyView.as_view(), name='about'),
]
