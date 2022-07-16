from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PrivateChatViewSet, MessageViewSet, PrivateChatJoinAPIView, CommentViewSet, CommentRatingViewSet

router = SimpleRouter()
router.register('comments', CommentViewSet, basename='comments')
router.register('comments_rating', CommentRatingViewSet, basename='comments rating')
router.register('messages', MessageViewSet, basename='messages')
router.register('private_chats', PrivateChatViewSet, basename='private chats')

urlpatterns = router.urls
urlpatterns.append(path('private_chats/join/<int:pk>/', PrivateChatJoinAPIView.as_view()),)

urlpatterns = format_suffix_patterns(urlpatterns)
