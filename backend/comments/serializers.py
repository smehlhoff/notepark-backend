from django.contrib.contenttypes.models import ContentType
from rest_framework import exceptions
from rest_framework import serializers

from backend.news.models import News
from backend.ultrabooks.models import Ultrabooks
from backend.users.utils import get_ip_address, get_user_agent
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    username = serializers.CharField(source='user.username', read_only=True)
    content_type = serializers.CharField(max_length=255, write_only=True)
    object_id = serializers.UUIDField(write_only=True)
    content = serializers.CharField(max_length=2500)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'username', 'content_type',
                  'object_id', 'content', 'created_at')

    def validate_content_type(self, value):
        valid_content = ['news', 'ultrabooks']

        if value not in valid_content:
            raise serializers.ValidationError(
                'This content type cannot save user comments.')

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

        if content_object.objects.filter(id=object_id, allow_comments=False):
            raise exceptions.PermissionDenied(
                'Posting comments has been disabled.')

        request = self.context.get('request', None)
        ip_address = get_ip_address(request)
        user_agent = get_user_agent(request)

        return Comment.objects.create(
            user=validated_data['user'],
            content_type=content_type_object,
            object_id=object_id,
            content=validated_data['content'],
            ip_address=ip_address,
            user_agent=user_agent,
        )


class CommentDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'username', 'content', 'created_at')


class ContentObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, News):
            return value.title
        elif isinstance(value, Ultrabooks):
            return value.name
        raise Exception('Unexpected type of content object.')


class UserCommentDetailSerialzier(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    content_type = serializers.CharField(
        source='content_type.model', read_only=True)
    name = ContentObjectRelatedField(source='content_object', read_only=True)
    slug = serializers.CharField(source='content_object.slug', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'username', 'content_type',
                  'content', 'name', 'slug', 'created_at')
