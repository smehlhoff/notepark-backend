from datetime import datetime

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Company, Ultrabooks
from .pagination import UltrabooksPagination, CompanyPagination, UltrabooksReleasedPagination
from .serializers import CompanySerializer, CompanyDetailSerializer, UltrabooksSerializer, UltrabooksDetailSerializer


class UltrabooksListView(generics.ListAPIView):
    queryset = Ultrabooks.objects.all()
    serializer_class = UltrabooksSerializer
    permission_classes = (AllowAny,)
    pagination_class = UltrabooksPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('@name', '$name')

    @method_decorator(cache_page(60 * 2))
    def dispatch(self, request, *args, **kwargs):
        return super(UltrabooksListView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return self.queryset.latest('created_at')


class UltrabooksReleasedListView(generics.ListAPIView):
    queryset = Ultrabooks.objects.all()
    serializer_class = UltrabooksSerializer
    permission_classes = (AllowAny,)
    pagination_class = UltrabooksReleasedPagination

    @method_decorator(cache_page(60 * 5))
    def dispatch(self, request, *args, **kwargs):
        return super(UltrabooksReleasedListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.exclude(launch_date__isnull=True).filter(launch_date__lte=datetime.utcnow())


class UltrabooksDetailView(generics.RetrieveAPIView):
    queryset = Ultrabooks.objects.all()
    serializer_class = UltrabooksDetailSerializer
    lookup_field = 'slug'
    permission_classes = (AllowAny,)


class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (AllowAny,)
    pagination_class = CompanyPagination

    @method_decorator(cache_page(60 * 5))
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyListView, self).dispatch(request, *args, **kwargs)


class CompanyDetailView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer
    lookup_field = 'slug'
    permission_classes = (AllowAny,)
