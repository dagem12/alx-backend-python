from rest_framework_nested import routers
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Create a router and register our viewsets with it
router = routers.NestedDefaultRouter()
conversations_router = router.register(r'conversations', ConversationViewSet)
conversations_router.register(
    r'messages',
    MessageViewSet,
    basename='conversation-messages',
    parents_query_lookups=['conversation']
)

urlpatterns = router.urls