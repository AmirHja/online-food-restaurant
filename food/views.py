from audioop import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from food.models import Food
from food.serializers import FoodSerializer, ShortFoodSerializer
from resturant.models import Restaurant
from users.models import Address



class HighRateFoodListView(APIView):
    @staticmethod
    def get(request):
        address_id = request.GET.get('address_id')
        try:
            address = Address.objects.get(pk=address_id)
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        city = address.city
        restaurants = Restaurant.objects.filter(city=city)
        foods = Food.objects.filter(restaurants__in=restaurants).order_by('-rate')[0:6]
        serializer = ShortFoodSerializer(foods, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class HighDiscountedFoodListView(APIView):
    @staticmethod
    def get(request):
        address_id = request.GET.get('address_id')
        try:
            address = Address.objects.get(pk=address_id)
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        city = address.city
        restaurants = Restaurant.objects.filter(city=city)
        foods = Food.objects.filter(restaurants__in=restaurants).order_by('-discount')[0:6]
        serializer = ShortFoodSerializer(foods, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FoodDetailView(APIView):
    @staticmethod
    def get(request):
        food_id = request.GET.get('food_id')
        try:
            food = Food.objects.get(pk=food_id)
        except Food.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FoodSerializer(food, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
