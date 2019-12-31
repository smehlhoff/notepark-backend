from rest_framework import exceptions
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteView(generics.CreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=None, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoriteRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    lookup_field = 'object_id'
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        try:
            Favorite.objects.get(user=self.request.user,
                                 object_id=self.kwargs['object_id'])
        except Favorite.DoesNotExist:
            raise exceptions.NotFound()

        return Response(data=None, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            favorite = Favorite.objects.get(
                user=self.request.user, object_id=self.kwargs['object_id'])
        except Favorite.DoesNotExist:
            raise exceptions.NotFound()

        favorite.delete()

        return Response(data=None, status=status.HTTP_204_NO_CONTENT)
