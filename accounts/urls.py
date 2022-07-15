from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserViewSet, ProfileDataViewSet, UserAvatarUpload

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('profiles', ProfileDataViewSet, basename='profiles')

urlpatterns = router.urls
urlpatterns.append(path('profile/upload/', UserAvatarUpload.as_view()),)

urlpatterns = format_suffix_patterns(urlpatterns)
