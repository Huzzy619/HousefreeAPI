from django.shortcuts import get_object_or_404
from rest_framework import generics, pagination, filters
from .serializers import BlogSerializer
from .models import Blog

class BlogListView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_object(self):
        return get_object_or_404(Blog, pk=self.kwargs.get('pk'))


