from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    class Meta:
        model = Payment
        fields =[
            'tracing_code',
            'amount',
            'status',
            'gateway',
            'date',
            'user'
        ]
