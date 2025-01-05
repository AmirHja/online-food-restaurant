from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import User
from payment.models import Payment
from .serilizer import PaymentSerializer

class PaymentView(APIView):
    @staticmethod
    def post(request):
        username = request.data.get('username')
        gateway = request.data.get('gateway')
        payment_status = request.data.get('status')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(data={'detail': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        amount = user.basket.total_basket_discounted_price()

        # SEND USER TO A PAYMENT TERMINAL

        payment = Payment.objects.create(user=user, amount=amount, status=payment_status, gateway=gateway)
        if payment:
            serializer = PaymentSerializer(payment)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data={'detail': 'payment is failed'}, status=status.HTTP_400_BAD_REQUEST)





