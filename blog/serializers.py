from rest_framework import serializers

from blog.models import Blog, Image


class BlogImageSerializer(serializers.ModelSerializer):
    img = serializers.ListField(child=serializers.ImageField(), allow_empty=False)

    class Meta:
        model = Image
        fields = ["id", "img"]

    def create(self, validated_data):

        images = validated_data.pop("img")

        pics = [Image(img=img, blog_id=self.context["blog_pk"]) for img in images]

        instance = Image.objects.bulk_create(pics)

        # Since the `instance` is a list, a key has to be assigned to the instance so it can be accessed in the View Response

        return {"image": instance}


class CreateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["id", "title", "content", "category", "featured"]

    def save(self, **kwargs):
        return super().save(author=self.context["user"], **self.validated_data)


class BlogSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True)  

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "content",
            "author",
            "date_published",
            "images",
            "featured",
        ]
