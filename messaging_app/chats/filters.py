import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.NumberFilter(field_name='sender__id')
    conversation = django_filters.NumberFilter(field_name='conversation__id')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'created_after', 'created_before']