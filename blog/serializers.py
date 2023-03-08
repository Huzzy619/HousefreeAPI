from rest_framework import serializers

from blog.models import Blog


class CreateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["id", "title", "content", "category", "featured", "image"]

    def save(self, **kwargs):
        return super().save(author=self.context["user"], **self.validated_data)


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "content",
            "author",
            "date_published",
            "image",
            "featured",
        ]
