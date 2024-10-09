from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='registration_page'),
    path('verify/', views.VerifyOTPView.as_view(), name='verify_page'),
    path('resend-otp/', views.ResendOTPView.as_view(), name='resend_otp_page'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password_page'),
    path('forgot-password-otp/', views.ResetPasswordOtpView.as_view(), name='forgot_password_otp_page'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password_page'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
