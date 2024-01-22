from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<ppk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<ppk>/like/<int:like>/', views.ProductLikeSetView.as_view(), name='set_product_like'),
    path('products/<ppk>/toggle-like/', views.ProductLikeToggleView.as_view(), name='toggle_product_like'),
]