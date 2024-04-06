from django.contrib import admin

from .models import Apartment, Bookmark, Media, Picture

admin.site.register([Bookmark, Picture, Media])


class PictureInline(admin.TabularInline):
    model = Picture
    extra = 2


class MediaInline(admin.TabularInline):
    model = Media
    extra = 1


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ["property_ref", "title", "category", "_type", "clicks"]
    inlines = [PictureInline, MediaInline]
