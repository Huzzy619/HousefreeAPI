from django.contrib import admin

# Register your models here.
from .models import Contact, Newsletter

admin.site.register([Contact, Newsletter])