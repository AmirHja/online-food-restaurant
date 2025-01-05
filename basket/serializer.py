from rest_framework import serializers

from basket.models import Basket
from food.models import Food



class ItemSerializer(serializers.ModelSerializer):
    price_after_discount = serializers.SerializerMethodField()
    restaurants = serializers.CharField(source='restaurants.name')
    class Meta:
        model = Food
        fields = [
            'id',
            'avatar',
            'name',
            'restaurants',
            'price',
            'discount',
            'price_after_discount'
        ]

    def get_price_after_discount(self, food):
        return food.price_after_discount()




class BasketSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    username = serializers.ReadOnlyField(source='user.username')
    real_price = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    class Meta:
        model = Basket
        fields = [
            'username',
            'items',
            'real_price',
            'discount',
            'discounted_price'

        ]

    def get_discounted_price(self, basket):
        return basket.total_basket_discounted_price()

    def get_real_price(self, basket):
        return basket.total_basket_price()

    def get_discount(self, basket):
        return basket.total_basket_discount()


