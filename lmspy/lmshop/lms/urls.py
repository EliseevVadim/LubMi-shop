from django.urls import path
from .views import *

app_name = 'lms'

urlpatterns = [
    path('admin/order/<slug:slug>/', AdminOrderView.as_view(), name='admin_order_details'),
    path('admin/order/<slug:slug>/complete-order/', AdminCompleteOrderView.as_view(), name='admin_complete_order'),
    path('admin/order/<slug:slug>/delivery-documents/', Admin_DeliveryDocuments_View.as_view(), name='admin_order_delivery_documents'),
    path('admin/action/customers/', Admin_Customers_View.as_view(), name='admin_customers'),
]
