from rest_framework import pagination


class CompanyPagination(pagination.PageNumberPagination):
    page_size = 12


class UltrabooksPagination(pagination.PageNumberPagination):
    page_size = 100


class UltrabooksReleasedPagination(pagination.PageNumberPagination):
    page_size = 10
