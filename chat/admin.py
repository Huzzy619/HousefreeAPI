from django.contrib import admin

# Register your models here.
from .models import Conversation, Message

admin.site.register([Conversation, Message])