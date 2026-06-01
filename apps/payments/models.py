from django.db import models
from django.conf import settings
from apps.orders.models import Order

class Payment(models.Model):
    class Provider(models.TextChoices):
        CLICK = 'click', 'Click'
        PAYME = 'payme', 'Payme'

    class Status(models.TextChoices):
        PENDING = 'pending', 'kutilmoqda'
        SUCCESS = 'success', 'muvaffaqiyatli'
        FAILED = 'failed', 'xato'
        CANCELLED = 'cancelled', 'bekor' 

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    provider = models.CharField(max_length=10, choices=Provider.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.provider} | {self.order.id} | {self.status}"