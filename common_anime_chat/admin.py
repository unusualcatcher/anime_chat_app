from django.contrib import admin
from .models import ChatRoom, Message, Friendship

admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(Friendship)