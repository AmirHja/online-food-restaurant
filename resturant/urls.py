from django.urls import path

from .models import Restaurant
from .views import NearbyRestaurant, AllRestaurants, GetRestaurant

urlpatterns = [
    path('api/restaurant/near/', NearbyRestaurant.as_view(), name='near-restaurant'),
    path('api/restaurant/all/', AllRestaurants.as_view(), name='all-restaurants'),
    path('api/restaurant/', GetRestaurant.as_view(), name='restaurant'),
]