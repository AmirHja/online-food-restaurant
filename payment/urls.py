from django.urls import path
from .views import PaymentView

urlpatterns = [
    path('api/payment/', PaymentView.as_view(), name='payment'),
]