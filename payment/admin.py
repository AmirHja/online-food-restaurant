from django.contrib import admin
from payment.models import Payment

# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['tracing_code', 'user', 'amount', 'status', 'gateway', 'date']
    ordering = ['tracing_code']
    list_filter = ['status', 'date']
    search_fields = ['user', 'tracing_code']
    date_hierarchy = 'date'
    raw_id_fields = ['user']
    list_editable = ['status']
    list_display_links = ['user', 'tracing_code']