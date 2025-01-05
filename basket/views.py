from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import User
from food.models import Food
from basket.models import Basket
from basket.serializer import *

class BasketView(APIView):
    @staticmethod
    def post(request):
        username = request.data.get('username')
        item_pk = request.data.get('food_id')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response('User does not exist', status=status.HTTP_404_NOT_FOUND)

        try:
             food = Food.objects.get(pk=item_pk)
        except Food.DoesNotExist:
            return Response('Food does not exist', status=status.HTTP_404_NOT_FOUND)

        try:
            basket = user.basket
        except Basket.DoesNotExist:
            basket = Basket.objects.create(user=user)

        if basket.items.all().count() == 0:
             basket.add_item(food.pk)

        else:
            basket_restaurant = basket.items.all()[0].restaurants
            if food.restaurants != basket_restaurant:
                return Response({'detail': 'You can\'t add food from several restaurant in one order'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                basket.add_item(item_pk)


        basket = Basket.objects.get(user=user)
        serializer = BasketSerializer(basket, context={'request': request})
        return Response(data= serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request):
        username = request.data.get('username')
        item_pk = request.data.get('food_id')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response('User does not exist', status=status.HTTP_404_NOT_FOUND)

        try:
            user.basket.delete_item(item_pk)
        except Basket.DoesNotExist:
            return Response('Food does not exist', status=status.HTTP_404_NOT_FOUND)

        basket = Basket.objects.get(user=user)
        serializer = BasketSerializer(basket, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def get(request):
        username = request.GET.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response('User does not exist', status=status.HTTP_404_NOT_FOUND)

        try:
            basket = user.basket
        except Basket.DoesNotExist:
            basket = Basket.objects.create(user=user)

        serializer = BasketSerializer(basket, context={'request': request})
        return Response(data= serializer.data, status=status.HTTP_200_OK)





