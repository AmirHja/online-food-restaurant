from django.urls import path

from .models import Restaurant
from .views import HighRateFoodListView, FoodDetailView, HighDiscountedFoodListView

urlpatterns = [
    path('api/food/best-rate/', HighRateFoodListView.as_view(), name='food_rate_list'),
    path('api/food/best-discount/', HighDiscountedFoodListView.as_view(), name='food_discount_list'),
    path('api/food/', FoodDetailView.as_view(), name='food_detail'),

    ]
