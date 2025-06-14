#!/usr/bin/env python3
"""Custom manager for filtering unread messages."""
from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.get_queryset().filter(receiver=user, read=False).only('id', 'sender', 'timestamp')  # ✅ .only()
