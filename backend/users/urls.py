from django.urls import path

from .views import SignUpView, UserRetrieveUpdateView, UserActivityView, SignInView, SignOutView, VerifyTokenView, \
    RefreshTokenView, ResetPasswordView, ResetPasswordConfirmView, UserProfileView

app_name = 'users'

urlpatterns = [
    path('users/', SignUpView.as_view()),
    path('users/me/', UserRetrieveUpdateView.as_view()),
    path('users/me/activity/', UserActivityView.as_view()),
    path('users/signin/', SignInView.as_view()),
    path('users/signout/', SignOutView.as_view()),
    path('users/verify-token/', VerifyTokenView.as_view()),
    path('users/refresh-token/', RefreshTokenView.as_view()),
    path('users/reset-password/', ResetPasswordView.as_view()),
    path('users/reset-password/confirm/', ResetPasswordConfirmView.as_view()),
    path('users/<username>/', UserProfileView.as_view()),
]
