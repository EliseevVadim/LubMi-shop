from django.urls import path
from .views import *

app_name = 'lms'

urlpatterns = [
    path('admin/order/<slug:slug>/', AdminOrderView.as_view(), name='admin_order_details'),
    path('admin/order/complete/<slug:slug>/', AdminCompleteOrderView.as_view(), name='admin_complete_order'),
]
