from django.urls import path
from .views import Login, SignUp, UserView, AddressView

urlpatterns = [
    path('api/login/', Login.as_view(), name='login'),
    path('api/signup/', SignUp.as_view(), name='signup'),
    # path('api/check-code/', CodeCheck.as_view(), name='code-check'),
    path('api/user/', UserView.as_view(), name='user'),
    path('api/address/', AddressView.as_view(), name='address'),
]