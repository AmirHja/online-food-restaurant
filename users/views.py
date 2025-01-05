from http.client import responses
from os import access
from turtledemo.sorting_animate import ssort
import random

from asgiref.timeout import timeout
from django.core.cache import cache
from django.contrib.auth import authenticate
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


from .models import User, Address
from .serializer import UserSerializer, AddressSerializer, AllUserSerializer

import random
import re
import uuid



class Login(APIView):
    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            serializer = UserSerializer(user)
            return Response(data={'username': serializer.data}, status=status.HTTP_200_OK)
        return Response(data={'detail': 'user does not found!'}, status=status.HTTP_400_BAD_REQUEST)

class SignUp(APIView):
    @staticmethod
    def post(request):
        phone_number = request.data.get('phone_number')
        print(type(phone_number))

        if phone_number is None:
            return Response(data={'detail': 'phone number required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(phone_number=phone_number).exists():
            return Response(data={'detail': 'user already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.search(r"^989[0-39]\d{8}$", str(phone_number)):
            return Response(data={'detail': 'Enter a valid phone number'},)


        code = random.randint(100_000, 999_999)
        code_key = f"otp_{phone_number}"
        cache.set(code_key, code, timeout=120)

        return Response(data={'phone_number': phone_number, 'code': code}, status=status.HTTP_200_OK)


# class CodeCheck(APIView):
#     @staticmethod
#     def post(request):
#         sent_code = request.data.get('code')
#         phone_number = request.data.get('phone_number')
#         code_key = f"otp_{phone_number}"
#         print(sent_code)
#         print(cache.get(code_key))
#
#         if sent_code is None:
#             return Response(data={'detail': 'code required'}, status=status.HTTP_400_BAD_REQUEST)
#
#         if sent_code != cache.get(code_key):
#             return Response(data={'detail': 'wrong code'}, status=status.HTTP_400_BAD_REQUEST)
#
#
#         return Response(data={'detail': 'correct code'}, status=status.HTTP_200_OK)


class UserView(APIView):
    @staticmethod
    def post(request):
        username = request.data.get('username')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        password = password1
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        gender = request.data.get('gender')

        if username is None:
            return Response(data={'detail': 'username required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response(data={'detail': 'username has already taken!'}, status=status.HTTP_400_BAD_REQUEST)

        if len(username) < 5:
            return Response(data={'detail': 'username must be at least 5 characters'}, status=status.HTTP_400_BAD_REQUEST)

        if username.isnumeric():
            return Response(data={'detail': 'username must be numeric'}, status=status.HTTP_400_BAD_REQUEST)

        if password1 != password2:
            return Response(data={'detail': 'passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        if password is None:
            return Response(data={'detail': 'password required'}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return Response(data={'detail': 'password must be at least 8 characters!'}, status=status.HTTP_400_BAD_REQUEST)

        if phone_number is None:
            return Response(data={'detail': 'phone number required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(phone_number=phone_number).exists():
            return Response(data={'detail': 'phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.search(r"^989[0-39]\d{8}$", str(phone_number)):
            return Response(data={'detail': 'Enter a valid phone number'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists() and (email is not None):
            print(User.objects.filter(email=email))
            return Response(data={'detail': 'email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if (email is not None) and (not re.search(r"^[a-zA-z0-9_.]+@[a-zA-z0-9_.]+\.[a-zA-z0-9_.]+$", email)):
            return Response(data={'detail': 'Enter a valid email address'},)

        if gender not in ['M', 'F', '']:
            return Response(data={'detail': 'Gender must be "M", "F" or empty string'}, status=status.HTTP_400_BAD_REQUEST)



        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name,
                                        phone_number=phone_number, email=email, gender=gender)
        context = {'username': user.username,
                   'password': user.password,
                   'first_name': first_name,
                   'last_name': last_name,
                   'phone_number': user.phone_number,
                   'email': user.email,
                   'gender': user.gender}
        return Response(data=context, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        username = request.GET.get('username')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(data={'detail': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(data={'detail': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddressView(APIView):
    @staticmethod
    def post(request):
        username = request.data.get('username')
        province = request.data.get('province')
        city = request.data.get('city')
        address = request.data.get('address')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(data={'detail': 'username does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        Address.objects.create(user=user, province=province, city=city, address=address)

        return Response(data={'detail': 'Address is added!'}, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        username = request.GET.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(data={'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        addresses = Address.objects.filter(user=user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request):
        id = request.data.get('id')
        address = Address.objects.get(pk=id)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request):
        id = request.query_params.get('id')
        try:
            address = Address.objects.get(pk=id)
        except Address.DoesNotExist:
            return Response(data={'detail': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)
        address.delete()
        return Response(data={'detail': 'Address deleted'}, status=status.HTTP_200_OK)














