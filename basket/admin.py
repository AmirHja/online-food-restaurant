from django.contrib import admin

from basket.models import Basket


# Register your models here.

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user']
    filter_horizontal = ['items']