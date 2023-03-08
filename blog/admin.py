from django.contrib import admin
from django.utils.html import format_html

from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "featured", "author_name", "show_image"]
    list_filter = ["category", "featured"]
    list_per_page = 10
    search_fields = [
        "title__icontains",
        "content__icontains",
        "category__istartswith",
        "author__first_name__istartswith",
    ]

    @admin.display(description="Blog Image")
    def show_image(self, instance):
        if instance.image:
            return format_html(
                f'<a href ="{instance.image.url}"><image src="{instance.image.url}" alt="{instance.title}" class = "thumbnail" ></a>'
            )
        return "no image"

    class Media:
        css = {"all": ["thumbnail/image.css"]}


