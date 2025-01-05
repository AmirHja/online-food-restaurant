from django.db import models
from rest_framework.templatetags.rest_framework import items

from resturant.models import Restaurant
from users.models import User
from food.models import Food

# Create your models here.

class Basket(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='basket')

    items = models.ManyToManyField(to=Food, related_name='basket', blank=True)

    def __str__(self):
        return self.user.username

    def total_basket_items(self):
        return self.items.all()

    def total_basket_discounted_price(self):
        total_basket_items = self.total_basket_items()
        price = 0
        for item in total_basket_items:
            price += item.price_after_discount()
        return price

    def total_basket_price(self):
        total_basket_items = self.total_basket_items()
        price = 0
        for item in total_basket_items:
            price += item.price
        return price

    def total_basket_discount(self):
        if self.total_basket_price() != 0:
            return ((self.total_basket_price() - self.total_basket_discounted_price()) / self.total_basket_price()) * 100
        else:
            return 0

    def delete_item(self, pk):
        item = Food.objects.get(pk=pk)
        self.items.remove(item)
        return items


    def delete_all(self):
        items = self.total_basket_items()
        for item in items:
            self.delete_item(item.pk)
        return items

    def add_item(self, pk):
        item = Food.objects.get(pk=pk)
        self.items.add(item)
        return self.total_basket_items()

