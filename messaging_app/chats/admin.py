from django.contrib import admin
from .models import CustomUser, Conversation, Message

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Conversation)
admin.site.register(Message)