from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    # -- products API --
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<str:order>/<int:pgs>/<int:pgn>/', views.ProductListPageView.as_view(), name='product_list_page'),
    path('products/<str:order>/<str:filter>/<int:pgs>/<int:pgn>/', views.ProductListPageView.as_view(), name='product_list_search_page'),
    path('products/<pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<ppk>/is-favorite/', views.ProductIsFavoriteView.as_view(), name='product_is_favorite'),
    path('products/<ppk>/like/<int:like>/', views.ProductLikeSetView.as_view(), name='set_product_like'),
    path('products/<ppk>/toggle-like/', views.ProductLikeToggleView.as_view(), name='toggle_product_like'),
    path('products/product/size/quantity/', views.ProductSizeQuantityView.as_view(), name='product_size_quantity'),
    # -- customer API --
    path('customer/info/<int:flags>/', views.GetCustomerInfoView.as_view(), name='get_customer_info'),
    path('customer/notify-me-product-delivery/', views.NotifyMeForDeliveryView.as_view(), name='notify_me_for_delivery'),
    path('customer/scart/', views.GetSCartView.as_view(), name='get_scart'),
    path('customer/add-product-to-scart/', views.ProductToSCartView.as_view(), name='product_to_scart'),
    path('customer/remove-product-from-scart/', views.KillProductInSCartView.as_view(), name='kill_product_in_scart'),
    path('customer/checkout/', views.CheckoutSCartView.as_view(), name='c6t'),
    path('customer/set-location/', views.SetLocationView.as_view(), name='set_location'),
    # -- Yookassa API --
    path('yookassa/payments/', views.YoPaymentsWebHookView.as_view(), name='yo_payments_webhook'),
]
