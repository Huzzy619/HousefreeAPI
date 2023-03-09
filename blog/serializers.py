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
            "author_name",
            "date_published",
            "image",
            "featured",
        ]
