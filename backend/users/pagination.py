from rest_framework import pagination


class UserActivityPagination(pagination.PageNumberPagination):
    page_size = 10
