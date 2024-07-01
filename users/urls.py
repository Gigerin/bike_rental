from django.urls import path
from .views import UserRegisterView, RegisterTemplateView, LoginTemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterTemplateView.as_view(), name='register_template'),
    path('api/register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginTemplateView.as_view(), name='login_template'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
