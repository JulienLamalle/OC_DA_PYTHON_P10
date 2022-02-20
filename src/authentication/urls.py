from django.urls import path

from authentication.views import RegistrationView, LoginView

urlpatterns = [
  path('signup/', RegistrationView.as_view(), name='signup'),
  path('login/', LoginView.as_view(), name='login'),
]
