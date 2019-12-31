from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import CommentSerializer


class CommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
