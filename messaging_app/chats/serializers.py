from rest_framework import serializers
from .models import CustomUser, Conversation, Message
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model"""
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=CustomUser.objects.all(),
            message="A user with this email already exists."
        )]
    )

    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 
                 'phone_number', 'password']
        read_only_fields = ['user_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        try:
            validate_password(value)
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the Message model"""
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'sender_username',
                 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at', 'sender_username']

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

    def validate_conversation(self, value):
        request = self.context.get('request')
        if request and request.user not in value.participants.all():
            raise serializers.ValidationError(
                "You must be a participant in this conversation to send messages."
            )
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for the Conversation model"""
    participants_detail = CustomUserSerializer(source='participants', 
                                            many=True, 
                                            read_only=True)
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participants_detail',
                 'created_at', 'updated_at', 'last_message']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least 2 participants."
            )
        return value

    def get_last_message(self, obj):
        last_message = Message.objects.filter(conversation=obj).order_by('-sent_at').first()
        if last_message:
            return MessageSerializer(last_message).data
        return None


class ConversationDetailSerializer(ConversationSerializer):
    """Detailed serializer for single conversation view with messages"""
    messages = MessageSerializer(many=True, read_only=True, source='message_set')

    class Meta(ConversationSerializer.Meta):
        fields = ConversationSerializer.Meta.fields + ['messages']