from rest_framework.routers import SimpleRouter
from django.views.generic import TemplateView
from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView)
from accounts.views import (
    AdministratorProfileAPIView, LoginViewSet, PasswordResetTokenCheck,
    RefreshViewSet, RegistrationViewSet, RequestPasswordResetEmail,
    SetNewPasswordAPIView, StudentProfileAPIView,
    StudentRegistrationViewSet, VerifyEmail)

app_name = "api"
routes = SimpleRouter()
# Accounts Routes
routes.register('login', LoginViewSet, basename='login')
routes.register('register', RegistrationViewSet, basename='register')
routes.register('auth/refresh', RefreshViewSet, basename='auth-refresh')
routes.register('password-reset', RequestPasswordResetEmail,
                basename="requestPasswordReset")
routes.register('password-reset-complete', SetNewPasswordAPIView,
                basename="password-reset-complete")
routes.register('student/register', StudentRegistrationViewSet,
                basename="patient-register")
routes.register('admin/profile', AdministratorProfileAPIView,
                basename="admin-profile")
routes.register('student/profile', StudentProfileAPIView,
                basename="student-profile")

urlpatterns = [
    *routes.urls,
    path('activate/', VerifyEmail,
         name="email-verify"),
    path('password-reset/<uidb64>/<token>', PasswordResetTokenCheck,
         name='password-reset-confirm'),
    path('password-reset-successful/',
         TemplateView.as_view(
             template_name="accounts/password_reset_success.html"),
         name="passwordResetSuccess"
         ),
]
