from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    # -- products API --
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<ppk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<ppk>/like/<int:like>/', views.ProductLikeSetView.as_view(), name='set_product_like'),
    path('products/<ppk>/toggle-like/', views.ProductLikeToggleView.as_view(), name='toggle_product_like'),
    # -- customer API --
    path('customer/info/<int:flags>/', views.GetCustomerInfoView.as_view(), name='get_customer_info'),
    path('customer/notify-me-product-delivery/', views.NotifyMeForDeliveryView.as_view(), name='notify_me_for_delivery'),
    path('customer/add-product-to-scart/', views.ProductToSCartView.as_view(), name='product_to_scart'),
    path('customer/remove-product-from-scart/', views.KillProductInSCartView.as_view(), name='kill_product_in_scart'),
    path('customer/checkout/', views.CheckoutSCartView.as_view(), name='c6t'),
    path('customer/set-location/', views.SetLocationView.as_view(), name='set_location'),
    # -- Yookassa API --
    path('yookassa/payments/', views.YoPaymentsWebHookView.as_view(), name='yo_payments_webhook'),
]
