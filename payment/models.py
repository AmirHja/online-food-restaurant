from django.db import models

from users.models import User

import uuid

def short_uuid():
    return str(uuid.uuid4())[0:15]


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'pending'
        SUCCESS = 'SUCCESS', 'success'
        FAILED = 'FAILED', 'failed'
        CANCELED = 'CANCELED', 'canceled'
        UNDER_REVIEW = 'UNDER_REVIEW', 'under review'
        REFUNDED = 'REFUNDED', 'refunded'
        EXPIRED = 'EXPIRED', 'expired'
        PROCESSING = 'PROCESSING', 'processing'
        DECLINED = 'DECLINED', 'declined'

    class Gateway(models.TextChoices):
        MELI = 'MELI', 'Meli'
        SAMAN =  'SAMAN', 'Saman'
        PASARGAD = 'PASARGAD', 'Pasargad'


    tracing_code = models.TextField(
        primary_key=True,
        null=False,
        blank=False,
        unique=True,
        default=short_uuid,
        max_length=20,
        editable=False
    )
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=7, decimal_places=0, default=0, editable=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    gateway = models.CharField(max_length=10, choices=Gateway.choices, default=Gateway.MELI)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def set_amount(self):
        self.amount = self.user.basket.total_basket_discounted_price()
