from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Payment
from apps.orders.models import Order
import hashlib


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        provider = request.data.get('provider', 'click')

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Buyurtma topilmadi'}, status=404)

        payment = Payment.objects.create(
            order=order,
            provider=provider,
            amount=order.total_price,
        )

        if provider == 'click':
            url = self._click_url(order, payment)
        elif provider == 'payme':
            url = self._payme_url(order, payment)
        else:
            return Response({'error': 'Noto\'g\'ri provider'}, status=400)

        return Response({
            'payment_id': payment.id,
            'payment_url': url,
            'amount': str(payment.amount),
            'provider': provider,
        })

    def _click_url(self, order, payment):
        merchant_id = settings.CLICK_MERCHANT_ID
        service_id = settings.CLICK_SERVICE_ID
        amount = int(order.total_price)
        return_url = settings.CLICK_RETURN_URL
        return (
            f"https://my.click.uz/services/pay"
            f"?service_id={service_id}"
            f"&merchant_id={merchant_id}"
            f"&amount={amount}"
            f"&transaction_param={payment.id}"
            f"&return_url={return_url}"
        )

    def _payme_url(self, order, payment):
        merchant_id = settings.PAYME_MERCHANT_ID
        amount = int(order.total_price) * 100  # tiyin
        return_url = settings.PAYME_RETURN_URL
        import base64
        params = f"m={merchant_id};ac.order_id={order.id};a={amount};c={return_url}"
        encoded = base64.b64encode(params.encode()).decode()
        return f"https://checkout.paycom.uz/{encoded}"


class ClickWebhookView(APIView):
    def post(self, request):
        payment_id = request.data.get('merchant_trans_id')
        status = request.data.get('error', '0')
        try:
            payment = Payment.objects.get(id=payment_id)
            if status == '0':
                payment.status = Payment.Status.SUCCESS
                payment.order.status = 'paid'
                payment.order.save()
            else:
                payment.status = Payment.Status.FAILED
            payment.save()
        except Payment.DoesNotExist:
            pass
        return Response({'error': 0})


class PaymeWebhookView(APIView):
    def post(self, request):
        method = request.data.get('method')
        params = request.data.get('params', {})

        if method == 'CheckPerformTransaction':
            return Response({'result': {'allow': True}})

        elif method == 'PerformTransaction':
            order_id = params.get('account', {}).get('order_id')
            try:
                order = Order.objects.get(id=order_id)
                order.status = 'paid'
                order.save()
                Payment.objects.filter(order=order).update(
                    status=Payment.Status.SUCCESS
                )
            except Order.DoesNotExist:
                pass
            return Response({'result': {'transaction': str(order_id)}})

        return Response({'result': {}})