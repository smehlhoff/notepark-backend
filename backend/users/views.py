from django.contrib.auth.signals import user_logged_in
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, UserActivity
from .pagination import UserActivityPagination
from .serializers import SignUpSerializer, SignInSerializer, UserProfileSerializer, UserSerializer, \
    ResetPasswordSerializer, ResetPasswordConfirmSerializer, UserActivitySerializer
from .utils import send_reset_password_email


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(generics.GenericAPIView):
    serializer_class = SignInSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            user_logged_in.send(sender=user.__class__,
                                request=request, user=user)

            return Response({
                'token': user.token
            }, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_403_FORBIDDEN)


class VerifyTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return Response(data=None, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        user.generate_token_identifier()

        return Response({
            'token': user.token
        }, status=status.HTTP_200_OK)


class SignOutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        user.generate_token_identifier()

        return Response(data=None, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'
    permission_classes = (AllowAny,)


class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=serializer.validated_data['email'])
            send_reset_password_email(user)

            return Response(data=None, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirmView(generics.GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            return Response(data=None, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivityView(generics.ListAPIView):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = UserActivityPagination

    def filter_queryset(self, queryset):
        return self.queryset.filter(user=self.request.user)
