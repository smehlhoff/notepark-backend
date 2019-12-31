from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from backend.comments.serializers import CommentDetailSerializer
from .models import Image, Ultrabooks, Company


class ImageSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'slug', 'created_at')


class UltrabooksSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ultrabooks
        fields = ('id', 'name', 'slug', 'company', 'launch_date', 'created_at')


class UltrabooksDetailSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField(read_only=True)
    company = serializers.StringRelatedField(read_only=True)
    design_colors = serializers.StringRelatedField(many=True, read_only=True)
    processor_models = serializers.StringRelatedField(
        many=True, read_only=True)
    video_card_models = serializers.StringRelatedField(
        many=True, read_only=True)
    memory_models = serializers.StringRelatedField(many=True, read_only=True)
    storage_models = serializers.StringRelatedField(many=True, read_only=True)
    operating_system_models = serializers.StringRelatedField(
        many=True, read_only=True)
    images = ImageSerialzier(many=True, read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    favorite_count = serializers.IntegerField(read_only=True)
    comments = CommentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Ultrabooks
        fields = ('id', 'content_type', 'name', 'slug', 'company', 'launch_date', 'weight', 'dimensions',
                  'design_colors', 'processor_models', 'video_card_models', 'memory_models', 'storage_models',
                  'display_size', 'display_resolution', 'battery', 'wireless', 'video', 'audio', 'connectivity',
                  'operating_system_models', 'optical_drive', 'features', 'images', 'allow_comments',
                  'display_comments', 'comment_count', 'comments', 'allow_favorites', 'display_favorites',
                  'favorite_count', 'created_at')

    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj).model

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if ret['display_comments'] is False:
            ret['comments'] = []

        ret['comment_count'] = len(ret['comments'])

        if ret['display_favorites'] is False:
            ret['favorite_count'] = 0

        return ret


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'slug', 'created_at')


class CompanyDetailSerializer(serializers.ModelSerializer):
    ultrabooks = UltrabooksSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'slug', 'ultrabooks', 'created_at')
