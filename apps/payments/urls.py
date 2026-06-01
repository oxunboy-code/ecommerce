from django.urls import path
from .views import CreatePaymentView, ClickWebhookView, PaymeWebhookView

urlpatterns = [
    path('create/', CreatePaymentView.as_view(), name='create-payment'),
    path('click/webhook/', ClickWebhookView.as_view(), name='click-webhook'),
    path('payme/webhook/', PaymeWebhookView.as_view(), name='payme-webhook'),
]