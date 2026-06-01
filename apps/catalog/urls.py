from django.urls import path
from .views import (
 CategoryListView, ProductListView, ProductDetailView, product_list_page, cart_page 
)
urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
]