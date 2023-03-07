from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import filters, pagination, permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Blog, Image
from .serializers import (BlogImageSerializer, BlogSerializer,
                          CreateBlogSerializer)

from .permissions import IsMarketerOrReadOnly
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
    permission_classes = [IsMarketerOrReadOnly]

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
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        # Since the images are returning null values in Response due to bulk_create,
        # a nice success message should suffice instead of instances of the newly uploaded images
        return Response(
            {"detail": " Blog Images uploaded successfully"}, status=status.HTTP_201_CREATED
        )
