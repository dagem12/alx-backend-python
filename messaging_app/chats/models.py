from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser.
    Add additional fields here if needed.
    """
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """
    A conversation between multiple users.
    """
    participants = models.ManyToManyField(CustomUser, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    """
    A message sent by a user in a conversation.
    """
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"
