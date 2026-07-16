from django.urls import path
from rest_framework_simplejwt.views import (
    
    TokenRefreshView,
)
from . import views
urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('password-change/',views.PasswordChangeView.as_view(),name='password-change'),
    path('profile/',views.ProfileView.as_view(),name="profile"),
    path('email-verify/',views.EmailVerifyView.as_view(),name='email-verify'),
]
