from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from backend.comments.serializers import CommentDetailSerializer
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'slug', 'comment_count', 'created_at')


class NewsDetailSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    comments = CommentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('id', 'content_type', 'title', 'slug', 'content', 'read_time', 'comment_count', 'comments',
                  'allow_comments', 'display_comments', 'created_at')

    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj).model

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if ret['display_comments'] is False:
            ret['comments'] = []

        ret['comment_count'] = len(ret['comments'])

        return ret
