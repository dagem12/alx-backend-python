from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer, 
    ConversationDetailSerializer,
    MessageSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling conversations
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all()

    def get_queryset(self):
        """Filter conversations to only those the user participates in"""
        return self.queryset.filter(participants=self.request.user)

    def get_serializer_class(self):
        """Use detailed serializer for retrieve action"""
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        return ConversationSerializer

    def perform_create(self, serializer):
        """Create a new conversation and add the creator as participant"""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling messages
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_queryset(self):
        """Filter messages to only those from conversations user participates in"""
        return self.queryset.filter(
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        """Create a new message with the current user as sender"""
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        """Custom create method to handle message creation"""
        conversation_id = request.data.get('conversation')
        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_id,
                participants=request.user
            )
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found or you're not a participant"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )