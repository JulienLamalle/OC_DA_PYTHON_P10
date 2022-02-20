from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
  def create_superuser(
      self, email, first_name=None, last_name=None, password=None, **other_fields
    ):

    other_fields.setdefault('is_staff', True)
    other_fields.setdefault('is_superuser', True)

    if other_fields.get('is_staff') is not True:
      raise ValueError(
          'Superuser must be assigned to is_staff=True.')
    if other_fields.get('is_superuser') is not True:
      raise ValueError(
          'Superuser must be assigned to is_superuser=True.')

    return self.create_user(email, first_name, last_name, password, **other_fields)

  def create_user(self, email, first_name=None, last_name=None, password=None, **other_fields):
    if not email:
      raise ValueError('You must provide an email address')

    email = self.normalize_email(email)
    user = self.model(email=email, first_name=first_name,
                      last_name=last_name, **other_fields)
    user.set_password(password)
    user.save()
    return user


class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(unique=True)
  first_name = models.CharField(max_length=150, blank=True)
  last_name = models.CharField(max_length=150, blank=True)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

  def __str__(self):
    return str(self.email)
  
  def get_tokens(self):
    refresh_token = RefreshToken.for_user(self)
    return {
      'refresh': str(refresh_token),
      'access': str(refresh_token.access_token)
    }