from django.contrib import admin
from food.models import Food

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurants', 'price', 'discount', 'rate']
    ordering = ('restaurants','price')
    list_filter = ['restaurants','price']
    search_fields = ['name', 'restaurants', 'description']
    raw_id_fields = ['restaurants']
    list_editable = ['price', 'discount']

# Register your models here.
