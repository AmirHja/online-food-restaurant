from django.contrib import admin
from resturant.models import Restaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'province', 'city', 'owner']
    ordering = ['name']
    search_fields = ['name', 'province', 'city', 'owner__username', 'address']
    raw_id_fields = ['owner']
    list_display_links = ['name', 'owner']
