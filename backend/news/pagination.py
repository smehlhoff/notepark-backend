from rest_framework import pagination


class NewsPagination(pagination.PageNumberPagination):
    page_size = 100
