from importlib.metadata import requires

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from resturant.models import Restaurant


class Food(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='images/foods', blank=True, null=True)
    rate = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),

        ],
        help_text="rate number (0 to 5)")
    restaurants = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE, related_name='foods', null=False, blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=0,)
    description = models.TextField(max_length=500, null=True, blank=True)
    discount = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        help_text="Discount percentage (0 to 100)")

    def price_after_discount(self):
        return (self.price * (100 - self.discount)) / 100



    def __str__(self):
        return self.name