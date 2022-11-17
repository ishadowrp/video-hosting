from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import MediaViewSet, MediaRatingViewSet, MediaChatJoinAPIView, MediaSearchAPIView, MediaOrderAPIView, \
    MediaByAuthorAPIView

router = SimpleRouter()
router.register('media', MediaViewSet, basename='media')
router.register('rating', MediaRatingViewSet, basename='media rating')

urlpatterns = router.urls
urlpatterns.append(path('media/join/<int:pk>/', MediaChatJoinAPIView.as_view()),)
urlpatterns.append(path('media/search', MediaSearchAPIView.as_view(), name='media search'),)
urlpatterns.append(path('media/author', MediaByAuthorAPIView.as_view(), name='media by author'),)
urlpatterns.append(path('media/order', MediaOrderAPIView.as_view(), name='media order'),)

urlpatterns = format_suffix_patterns(urlpatterns)
