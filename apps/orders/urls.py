from django.urls import path
from .views import CartView, OrderListCreateView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('orders/', OrderListCreateView.as_view(), name='orders'),
]