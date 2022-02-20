from .models import User
from rest_framework import serializers
from django.contrib import auth


class RegistrationSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required=True)
  password_confirmation = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = User
    fields = ['email', 'first_name', 'last_name',
              'password', 'password_confirmation']

  def validate(self, data):
    print(data)
    if data['password_confirmation'] != data['password']:
      raise serializers.ValidationError(
        'Password confirmation does not match.')
    return data

  def create(self, validated_data):
    return User.objects.create_user(first_name=validated_data['first_name'], last_name=validated_data['last_name'], email=validated_data['email'], password=validated_data['password'])


class LoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(required=True)
  password = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = User
    fields = ['email', 'password']

  def validate(self, data):
    email = data['email']
    password = data['password']

    user = auth.authenticate(email=email, password=password)

    if not user or not user.is_active:
      raise serializers.ValidationError('Invalid Credentials')

    return {
      'email': user.email,
      'first_name': user.first_name,
      'last_name': user.last_name,
      'tokens': user.get_tokens()
    }


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'first_name', 'last_name']
