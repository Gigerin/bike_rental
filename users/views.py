from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class RegisterTemplateView(TemplateView):
    template_name = "users/register.html"

class LoginTemplateView(TemplateView):
    template_name = "users/login.html"
