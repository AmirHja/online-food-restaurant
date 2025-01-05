from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Restaurant
from food.models import Food
from food.serializers import FoodSerializer




class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'avatar'
        ]


class SingleRestaurantSerializer(serializers.ModelSerializer):
    foods = FoodSerializer(many=True)
    owner = serializers.CharField(source='owner.username')
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'description',
            'avatar',
            'owner',
            'address',
            'foods'
        ]