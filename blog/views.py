from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import filters, pagination, permissions
from rest_framework.viewsets import ModelViewSet

from .models import Blog, Image
from .serializers import (BlogImageSerializer, BlogSerializer,
                          CreateBlogSerializer)


class BlogViewSet(ModelViewSet):

    queryset = Blog.objects.all()
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["title", "content", "category"]
    ordering_fields = ["date_published", "date_updated"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return BlogSerializer
        return CreateBlogSerializer

    def get_serializer_context(self):
        return {"user": self.request.user, "request": self.request}


@extend_schema(
    parameters=[
        OpenApiParameter(name="id", description="Image id", required=True, type=int),
    ]
)
class ImageViewSet(ModelViewSet):
    http_method_names = ["post", "get", "delete"]
    serializer_class = BlogImageSerializer

    def get_queryset(self):
        if pk := self.kwargs.get("blog_pk", ""):
            return Image.objects.filter(blog_id=pk)
        return Image.objects.none()

    def get_serializer_context(self):
        context = {"request", self.request}

        if pk := self.kwargs.get("blog_pk", ""):
            context["blog_pk"] = pk
        return context
