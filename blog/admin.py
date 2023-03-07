from django.contrib import admin
from .models import Blog, Image
from django.utils.html import format_html

# Register your models here.

class ImageInline(admin.TabularInline):
    model = Image
    readonly_fields = ['blog_img']
    extra = 0

    def blog_img(self, instance):
        return format_html(f'<a href ="{instance.img.url}"><img src="{instance.img.url}" alt="{instance.blog.title}" class = "thumbnail" ></a>')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'featured', 'author_name']
    list_filter = ["category", "featured"]
    list_per_page = 10
    inlines = [ImageInline]
    search_fields = ['title__icontains', 'content__icontains', 'category__istartswith', 'author__first_name__istartswith']
    

    class Media:
        css = {
            'all': ['thumbnail/image.css']
        }

# admin.site.register(Image)

