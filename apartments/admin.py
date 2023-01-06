from django.contrib import admin
from .models import Bookmark, Apartment, Picture
# Register your models here.

admin.site.register([Bookmark, Apartment, Picture])
