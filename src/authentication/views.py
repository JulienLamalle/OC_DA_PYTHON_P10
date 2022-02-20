from django.shortcuts import render
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegistrationSerializer, LoginSerializer

from .models import User

class RegistrationView(generics.GenericAPIView):
  permissions_classes = [AllowAny]
  serializer_class = RegistrationSerializer
  
  @transaction.atomic
  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid(raise_exception=True):
      user = serializer.save()
      RefreshToken.for_user(user).access_token
      user_to_return = { "email": user.email, "first_name": user.first_name, "last_name": user.last_name, "access_token": str(RefreshToken.for_user(user).access_token)}
      return Response(user_to_return, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
class LoginView(generics.GenericAPIView):
  permission_classes = [AllowAny]
  serializer_class = LoginSerializer
  
  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid(raise_exception=True):
      user = serializer.validated_data
      return Response(user, status=status.HTTP_200_OK)