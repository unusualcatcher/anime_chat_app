from django.db import models
from users.models import Profile

class AsyncChatRoomQuerySet(models.QuerySet):
    async def get_chatroom_by_name(self, name):
        try:
            return await self.get(name=name)
        except self.model.DoesNotExist:
            return None

    async def get_messages_for_chatroom(self, chatroom):
        return await Message.objects.filter(chat_room=chatroom).order_by('timestamp')

class AsyncChatRoomManager(models.Manager):
    _queryset_class = AsyncChatRoomQuerySet

    def get_queryset(self):
        return self._queryset_class(self.model, using=self._db)

    async def get_chatroom_by_name(self, name):
        return await self.get_queryset().get_chatroom_by_name(name)

    async def get_messages_for_chatroom(self, chatroom):
        return await self.get_queryset().get_messages_for_chatroom(chatroom)
class ChatRoom(models.Model):
    name = models.CharField(max_length=150, unique=False)
    participants = models.ManyToManyField(Profile)
    objects = models.Manager()  # Synchronous manager
    async_objects = AsyncChatRoomManager()

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Friendship(models.Model):
    sender = models.ForeignKey(Profile, related_name='friendship_sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name='friendship_receiver', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted')])
    blocked = models.BooleanField(default=False)

    class Meta:
        unique_together = ['sender', 'receiver']
