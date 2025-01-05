from django.urls import path

from .views import OrderDetailView, OrderListView

urlpatterns = [
    path('api/order/detail/', OrderDetailView.as_view(), name='order-detail'),
    path('api/order/', OrderListView.as_view(), name='order-list'),
]