from django.contrib import admin
from .models import Bookmark, Apartment
# Register your models here.

admin.site.register([Bookmark, Apartment])
