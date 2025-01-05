from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import User, Address
from payment.models import Payment
from .models import Order
from .serializers import OrderDetailSerializer, OrderListSerializer


class OrderListView(APIView):
    @staticmethod
    def get(request):  # Get list of orders
        username = request.GET.get('username')
        if username == '-1':
            orders = Order.objects.all()
            serializer = OrderListSerializer(orders, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        user = User.objects.get(username=username)
        payments = Payment.objects.filter(user=user)
        orders = Order.objects.filter(payment__in=payments)
        serializer = OrderListSerializer(orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)



    @staticmethod
    def post(request):  # Add an order list
        username = request.data.get('username')
        tracing_code = request.data.get('tracing_code')
        address_id = request.data.get('address_id')


        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(data={'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        try:
            payment = Payment.objects.get(tracing_code=tracing_code)
        except Payment.DoesNotExist:
            return Response(data={'detail': 'Payment does not exist'}, status=status.HTTP_404_NOT_FOUND)

        try:
            address = Address.objects.get(pk=address_id)
        except Address.DoesNotExist:
            return Response(data={'detail': 'Address does not exist'}, status=status.HTTP_404_NOT_FOUND)


        basket = user.basket

        if payment.status == "SUCCESS" and basket.items.count() != 0 and payment.amount == basket.total_basket_discounted_price():
            order = Order.objects.create(payment=payment,
                                         restaurant=basket.items.all()[0].restaurants,
                                         address=address,
                                         amount=payment.amount)

            food_item_ids = basket.items.values_list('pk', flat=True)
            order.items.set(food_item_ids)
            print("$" * 100)
            if order: basket.delete_all()
            serializer = OrderDetailSerializer(order)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data={'detail': 'Payment is invalid'}, status=status.HTTP_400_BAD_REQUEST)



class OrderDetailView(APIView):
    @staticmethod
    def get(request):
        pk = request.GET.get('order_id')
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(data={'detail': 'order has not been found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderDetailSerializer(order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

