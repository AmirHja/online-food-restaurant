from rest_framework import serializers

from order.models import Order
from food.serializers import ShortFoodSerializer, ItemsAvatarSerializer
from users.serializer import AddressSerializer



class OrderDetailSerializer(serializers.ModelSerializer):
    restaurant = serializers.CharField(source='restaurant.name')
    address = AddressSerializer()
    items = ShortFoodSerializer(many=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'payment',
            'restaurant',
            'address',
            'amount',
            'items'
        ]



class OrderListSerializer(serializers.ModelSerializer):
    restaurant = serializers.CharField(source='restaurant.name')
    date = serializers.SerializerMethodField()
    items = ItemsAvatarSerializer(many=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'restaurant',
            'date',
            'payment',
            'amount',
            'items'

        ]

    def get_date(self, order):
        return order.payment.date