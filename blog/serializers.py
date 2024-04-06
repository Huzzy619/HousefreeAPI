from rest_framework import serializers

from blog.models import Blog


class CreateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["id", "title", "content", "category", "featured", "image"]


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "content",
            "category",
            "author_name",
            "created_at",
            "image",
            "featured",
        ]
