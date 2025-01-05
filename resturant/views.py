from itertools import count

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Restaurant
from .serializers import RestaurantSerializer, SingleRestaurantSerializer
from users.models import Address



class NearbyRestaurant(APIView):
    @staticmethod
    def get(request):
        address_id = request.GET.get('address_id')
        address = Address.objects.get(pk=address_id)
        restaurants = Restaurant.objects.filter(city=address.city)[0:5]
        serializer = RestaurantSerializer(restaurants, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AllRestaurants(APIView):
    @staticmethod
    def get(request):
        address_id = request.GET.get('address_id')
        address = Address.objects.get(pk=address_id)
        restaurants = Restaurant.objects.filter(city=address.city)
        serializer = RestaurantSerializer(restaurants, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetRestaurant(APIView):
    @staticmethod
    def get(request):
        restaurant_id = request.GET.get('restaurant_id')
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        serializer = SingleRestaurantSerializer(restaurant, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
