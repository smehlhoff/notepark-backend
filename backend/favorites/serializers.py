from django.contrib.contenttypes.models import ContentType
from rest_framework import exceptions
from rest_framework import serializers

from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    content_type = serializers.CharField(max_length=255, write_only=True)
    object_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Favorite
        fields = ('user', 'content_type', 'object_id')

    def validate_content_type(self, value):
        valid_content = ['ultrabooks']

        if value not in valid_content:
            raise serializers.ValidationError(
                'This content type cannot be saved to favorites.')

        return value

    def create(self, validated_data):
        content_type = validated_data['content_type']
        object_id = validated_data['object_id']

        try:
            content_model_name = ContentType.objects.get(model=content_type)
        except ContentType.DoesNotExist:
            raise serializers.ValidationError({
                'content_type': ['This id is invalid.']
            })

        content_object = content_model_name.model_class()
        content_type_object = ContentType.objects.get_for_model(content_object)

        if not content_object.objects.filter(id=object_id).exists():
            raise serializers.ValidationError({
                'object_id': ['This id is invalid.']
            })

        if Favorite.objects.filter(user=validated_data['user'], object_id=object_id).exists():
            raise exceptions.ParseError(
                'This object is already saved to favorites.')

        if content_object.objects.filter(id=object_id, allow_favorites=False):
            raise exceptions.PermissionDenied(
                'Saving this object as a favorite has been disabled.')

        return Favorite.objects.create(
            user=validated_data['user'],
            content_type=content_type_object,
            object_id=object_id,
        )


class UserFavoriteDetailSerialzier(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    content_type = serializers.CharField(
        source='content_type.model', read_only=True)
    name = serializers.CharField(source='content_object.name', read_only=True)
    slug = serializers.CharField(source='content_object.slug', read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'username', 'content_type',
                  'name', 'slug', 'created_at')
