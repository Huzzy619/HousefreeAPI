from django.contrib import admin
from .models import Bookmark, Apartment, Picture


admin.site.register([Bookmark, Apartment, Picture])
