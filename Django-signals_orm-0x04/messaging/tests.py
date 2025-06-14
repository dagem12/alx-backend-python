from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageSignalTest(TestCase):
    def test_notification_created_on_message(self):
        sender = User.objects.create(username='sender')
        receiver = User.objects.create(username='receiver')
        message = Message.objects.create(sender=sender, receiver=receiver, content="Hello")
        self.assertEqual(Notification.objects.filter(user=receiver).count(), 1)