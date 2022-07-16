from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import MediaViewSet, MediaRatingViewSet, MediaChatJoinAPIView

router = SimpleRouter()
router.register('media', MediaViewSet, basename='media')
router.register('media/rating', MediaRatingViewSet, basename='media rating')

urlpatterns = router.urls
urlpatterns.append(path('media/join/<int:pk>/', MediaChatJoinAPIView.as_view()),)

urlpatterns = format_suffix_patterns(urlpatterns)
