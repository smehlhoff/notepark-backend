import re

from rest_framework import serializers

from backend.users.utils import get_ip_address, get_user_agent
from .models import Ticket, CATEGORIES


class TicketSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255, trim_whitespace=False, write_only=True)
    email = serializers.EmailField(max_length=255, write_only=True)
    category = serializers.ChoiceField(choices=CATEGORIES, write_only=True)
    content = serializers.CharField(max_length=2500, write_only=True)

    class Meta:
        model = Ticket
        fields = ('name', 'email', 'category', 'content')

    def validate_name(self, value):
        if not re.match('^[a-zA-Z ]+$', value):
            raise serializers.ValidationError('A valid name is required.')

        return value

    def create(self, validated_data):
        request = self.context.get('request', None)
        ip_address = get_ip_address(request)
        user_agent = get_user_agent(request)

        return Ticket.objects.create(ip_address=ip_address, user_agent=user_agent, **validated_data)
