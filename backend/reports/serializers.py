from django.contrib.contenttypes.models import ContentType
from rest_framework import exceptions
from rest_framework import serializers

from .models import Report, CATEGORIES


class ReportSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    content_type = serializers.CharField(max_length=255, write_only=True)
    object_id = serializers.UUIDField(write_only=True)
    category = serializers.ChoiceField(choices=CATEGORIES, write_only=True)

    class Meta:
        model = Report
        fields = ('user', 'content_type', 'object_id', 'category')

    def validate_content_type(self, value):
        valid_content = ['comment']

        if value not in valid_content:
            raise serializers.ValidationError(
                'This content type cannot save user reports.')

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

        if Report.objects.filter(user=validated_data['user'], object_id=object_id).exists():
            raise exceptions.ParseError(
                'This comment has already been reported.')

        return Report.objects.create(
            user=validated_data['user'],
            content_type=content_type_object,
            object_id=object_id,
            category=validated_data['category'],
        )
