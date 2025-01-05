from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from food.models import Food

class ShortFoodSerializer(serializers.ModelSerializer):
    price_after_discount = serializers.SerializerMethodField()
    restaurants = serializers.CharField(source='restaurants.name')
    class Meta:
        model = Food
        fields = [
            'id',
            'rate',
            'name',
            'avatar',
            'restaurants',
            'price',
            'discount',
            'price_after_discount'
        ]

    def get_price_after_discount(self, food):
        return food.price_after_discount()


class FoodSerializer(serializers.ModelSerializer):
    price_after_discount = serializers.SerializerMethodField()
    class Meta:
        model = Food
        fields = [
            'id',
            'rate',
            'name',
            'avatar',
            'description',
            'price',
            'discount',
            'price_after_discount'
        ]

    def get_price_after_discount(self, food):
        return food.price_after_discount()

class ItemsAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = [
            'id',
            'avatar'
        ]