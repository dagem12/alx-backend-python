import django_filters
from .models import Message
from django.utils.timezone import now

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.NumberFilter(field_name="sender__id")
    start_time = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'start_time', 'end_time']