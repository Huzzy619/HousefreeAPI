from rest_framework import serializers
from blog.models import Blog


class CreateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title','content' ,'category', 'image', 'featured']
    
    
    def save(self, **kwargs):
        return super().save(author = self.context['user'], **self.validated_data)

class BlogSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author', 'date_published', 'image', 'featured']
    
    def get_image(self, obj):
        try:
            return self.context["request"].build_absolute_uri(obj.image.url)
        except:
            return None
