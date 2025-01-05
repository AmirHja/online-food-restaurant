from django.contrib import admin
from order.models import Order
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['payment']
    raw_id_fields = ['payment']
    filter_horizontal = ['items']