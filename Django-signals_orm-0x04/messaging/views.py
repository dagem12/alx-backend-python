#!/usr/bin/env python3
"""Views for messaging system."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

@login_required
def delete_user(request):
    """
    Allows a logged-in user to delete their own account.
    """
    user = request.user
    user.delete()
    return redirect('home')

@login_required
def conversation_view(request, receiver_id):
    """
    Displays messages between current user and another user,
    with threaded replies shown recursively.
    """
    receiver = User.objects.get(id=receiver_id)

    # Fetch top-level messages (not replies) between the two users
    messages = Message.objects.filter(
        sender=request.user,
        receiver=receiver,
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related('replies__sender', 'replies__receiver')

    context = {
        'messages': messages,
        'receiver': receiver
    }
    return render(request, 'messaging/conversation.html', context)

    def inbox_view(request):
    """
    Displays unread messages for the logged-in user.
    """
    unread_messages = Message.unread.unread_for_user(request.user)
    return render(request, 'messaging/inbox.html', {'unread_messages': unread_messages})