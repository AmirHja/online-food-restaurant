from django.db import models
from rest_framework.templatetags.rest_framework import items

from food.models import Food
from payment.models import Payment
from resturant.models import Restaurant
from users.models import Address


# Create your models here.

class Order(models.Model):
        payment = models.OneToOneField(to=Payment, on_delete=models.CASCADE,
                                       null=False, blank=False, related_name='order')  # order code

        items = models.ManyToManyField(to=Food, related_name='orders')

        restaurant = models.ForeignKey(to=Restaurant, on_delete=models.DO_NOTHING,  blank=True, null=True, related_name='orders')
        address = models.ForeignKey(to=Address, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='orders')
        amount = models.IntegerField(default=0, null=False, blank=False)

        def __str__(self):
                return str(self.payment)

        def set_restaurant(self):
                if self.items.count() != 0: self.restaurant = self.items.all()[0].restaurants
                else: self.restaurant = None
                return self.restaurant

        # def save(self, *args, **kwargs):
        #         self.set_restaurant()
        #         super(Order, self).save(*args, **kwargs)