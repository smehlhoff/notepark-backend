from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import TicketSerializer


class TicketView(generics.CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=None, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
