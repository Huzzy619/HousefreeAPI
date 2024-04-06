from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, pagination, permissions
from rest_framework.viewsets import ModelViewSet

from .models import Blog
from .permissions import IsMarketerOrReadOnly
from .serializers import BlogSerializer, CreateBlogSerializer


class BlogViewSet(ModelViewSet):
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    http_method_names = ["post", "get", "delete", "patch"]
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [IsMarketerOrReadOnly]
    queryset = Blog.objects.all()
    ordering_fields = ["created_at", "updated_at"]
    search_fields = ["title", "content", "category"]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return BlogSerializer
        return CreateBlogSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
