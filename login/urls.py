from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenBlacklistView)
from .views import UserCreateView, UserDetailView, CompanyView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('logout/', TokenBlacklistView.as_view()),
    path('user/', UserCreateView.as_view()),
    path('user/<int:pk>/', UserDetailView.as_view()),
    path('company', CompanyView.companyAPI),
    path('company/<int:id>', CompanyView.companyAPI)
]