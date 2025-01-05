from django.db import models

from users.models import User


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=25)
    province = models.CharField(max_length=25)
    address = models.CharField(max_length=250)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='restaurant')
    avatar = models.ImageField(upload_to='images/restaurants', blank=True, null=True)


    def __str__(self):
        return self.name

