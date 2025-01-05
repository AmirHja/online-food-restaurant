from django.urls import path

from .models import Basket
from .views import BasketView

urlpatterns = [
    path('api/basket/', BasketView.as_view(), name='add-basket'),
]