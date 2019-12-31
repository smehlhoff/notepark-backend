import re

from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import exceptions
from rest_framework import serializers

from backend.comments.models import Comment
from backend.comments.serializers import UserCommentDetailSerialzier
from backend.favorites.models import Favorite
from backend.favorites.serializers import UserFavoriteDetailSerialzier
from config.blacklist import USERNAME_BLACKLIST
from .models import User, UserActivity
from .utils import send_password_changed_email


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=3, max_length=15, write_only=True)
    email = serializers.EmailField(max_length=255, write_only=True)
    password = serializers.CharField(
        min_length=8, max_length=255, write_only=True)
    confirm_password = serializers.CharField(
        min_length=8, max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'token')

    def validate_username(self, value):
        username = value.lower()

        if not re.match('^[a-zA-Z0-9]+$', username):
            raise serializers.ValidationError('A valid username is required.')

        if username in USERNAME_BLACKLIST:
            raise serializers.ValidationError(
                'This username is not acceptable.')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('This username already exists.')

        return username

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'This email address already exists.')

        return value

    def validate(self, attrs):
        password = attrs.get('password', None)
        confirm_password = attrs.get('confirm_password', None)

        if confirm_password != password:
            raise serializers.ValidationError({
                'confirm_password': ['Please confirm your password.']
            })

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['confirm_password'],
            email=validated_data['email']
        )


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate_username(self, value):
        if not re.match('^[a-zA-Z0-9]+$', value):
            raise serializers.ValidationError('A valid username is required.')

        return value

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)

        user = authenticate(username=username, password=password)

        if user is None:
            raise exceptions.AuthenticationFailed(
                'Username and password is invalid.')

        if user.is_banned:
            raise exceptions.AuthenticationFailed(
                'This account has been banned.')

        attrs['user'] = user

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    ultrabook = serializers.CharField(
        read_only=True, source='profile.ultrabook')
    location = serializers.CharField(read_only=True, source='profile.location')
    bio = serializers.CharField(read_only=True, source='profile.bio')
    comments = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    favorites = serializers.SerializerMethodField(read_only=True)
    favorite_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'ultrabook', 'location', 'bio', 'comments',
                  'comment_count', 'favorites', 'favorite_count', 'date_joined')

    def get_comments(self, obj):
        comments = Comment.objects.filter(user=obj)

        return UserCommentDetailSerialzier(comments, many=True, read_only=True).data

    def get_favorites(self, obj):
        favorites = Favorite.objects.filter(user=obj)

        return UserFavoriteDetailSerialzier(favorites, many=True, read_only=True).data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['comment_count'] = len(ret['comments'])
        ret['favorite_count'] = len(ret['favorites'])

        return ret


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=3, max_length=15, required=False)
    email = serializers.EmailField(max_length=255, required=False)
    first_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    last_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    ultrabook = serializers.CharField(
        max_length=255, source='profile.ultrabook', required=False, allow_blank=True)
    location = serializers.CharField(
        max_length=255, source='profile.location', required=False, allow_blank=True)
    bio = serializers.CharField(
        max_length=2500, source='profile.bio', required=False, allow_blank=True)
    password = serializers.CharField(required=False, write_only=True)
    new_password = serializers.CharField(
        min_length=8, max_length=255, required=False, write_only=True)
    confirm_new_password = serializers.CharField(
        min_length=8, max_length=255, required=False, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'ultrabook', 'location', 'bio', 'password',
                  'new_password', 'confirm_new_password')

    def validate_username(self, value):
        username = value.lower()

        if not re.match('^[a-zA-Z0-9]+$', username):
            raise serializers.ValidationError('A valid username is required.')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('This username already exists.')

        return username

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'This email address already exists.')

        return value

    def validate_first_name(self, value):
        if not re.match('^$|^[a-zA-Z0-9]+$', value):
            raise serializers.ValidationError(
                'A valid first name is required.')

        return value

    def validate_last_name(self, value):
        if not re.match('^$|^[a-zA-Z0-9]+$', value):
            raise serializers.ValidationError('A valid last name is required.')

        return value

    def validate(self, attrs):
        new_password = attrs.get('new_password', None)
        confirm_new_password = attrs.get('confirm_new_password', None)

        if confirm_new_password != new_password:
            raise serializers.ValidationError({
                'confirm_new_password': ['Please confirm your new password.']
            })

        return attrs

    def update(self, instance, validated_data):
        username = instance.username
        new_username = validated_data.pop('username', None)
        new_email = validated_data.pop('email', None)
        profile = validated_data.pop('profile', {})
        password = validated_data.pop('password', None)
        new_password = validated_data.pop('new_password', None)
        confirm_new_password = validated_data.pop('confirm_new_password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if new_username and password is not None:
            user = authenticate(username=username, password=password)

            if user is None:
                raise exceptions.NotAuthenticated(
                    'Your password is incorrect.')

            instance.username = new_username
            instance.generate_token_identifier()

        if new_email and password is not None:
            user = authenticate(username=username, password=password)

            if user is None:
                raise exceptions.NotAuthenticated(
                    'Your password is incorrect.')

            instance.email = new_email

        if password and new_password and confirm_new_password is not None:
            user = authenticate(username=username, password=password)

            if user is None:
                raise exceptions.NotAuthenticated(
                    'Your old password is incorrect.')

            instance.set_password(confirm_new_password)
            instance.generate_token_identifier()

            send_password_changed_email(user)

        instance.save()

        for attr, value in profile.items():
            setattr(instance.profile, attr, value)

        instance.profile.save()

        return instance


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, write_only=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'This email address is not associated with an account.')

        return value


class ResetPasswordConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=8, max_length=255, write_only=True)
    confirm_password = serializers.CharField(
        min_length=8, max_length=255, write_only=True)
    uid = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password', None)
        confirm_password = attrs.get('confirm_password', None)

        if confirm_password != password:
            raise serializers.ValidationError({
                'confirm_password': ['Please confirm your new password.']
            })

        try:
            uid = force_text(urlsafe_base64_decode(attrs['uid']))
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({
                'uid': ['This token is not associated with an account.']
            })

        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError({
                'token': ['This token is invalid.']
            })

        if user.is_banned:
            raise exceptions.AuthenticationFailed(
                'This account has been banned.')

        user.set_password(confirm_password)
        user.generate_token_identifier()
        user.save()

        return attrs


class UserActivitySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserActivity
        fields = ('id', 'username', 'ip_address', 'user_agent', 'created_at')
