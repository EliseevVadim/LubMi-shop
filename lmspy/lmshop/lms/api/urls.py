from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<pk>/like/<int:like>/', views.ProductLike.as_view(), name='product_like'),
]