from rest_framework import serializers
from blog.models import Blog, Image


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "img"]
    
    def save(self, **kwargs):
        return super().save(blog_id = self.context['blog_pk'], **kwargs)

class CreateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id','title','content' ,'category', 'featured']
    
    
    def save(self, **kwargs):
        return super().save(author = self.context['user'], **self.validated_data)

class BlogSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many = True) #serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author', 'date_published', 'images', 'featured']
    
    # def get_image(self, obj):
    #     try:
    #         return self.context["request"].build_absolute_uri(obj.image.url)
    #     except:
    #         return None
