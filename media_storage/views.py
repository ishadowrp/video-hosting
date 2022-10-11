from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

from accounts.permissions import IsOwnerOrReadOnly

from .serializers import MediaSerializer, MediaRatingSerializer
from .models import Media, MediaRating
from comments_and_chats.models import Comment


class MediaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated,)
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    filterset_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MediaChatJoinAPIView(APIView):
    permissions_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get_object(pk):
        try:
            return Media.objects.get(pk=pk)
        except Media.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        media = self.get_object(pk)
        comments = Comment.objects.filter(media__id=pk)
        media.views_count += 1
        media.save()

        list_of_comments = []
        for item in comments:
            dict_message = {'author': item.author.username, 'author_id': item.author.pk,
                            'date_posted': item.date_posted.strftime("%d-%m-%Y %H:%M:%S"), 'content': item.content}
            list_of_comments.append(dict_message)

        dict_response = {'chat': pk, 'title': media.title, 'comments': list_of_comments}

        return Response(dict_response, status=status.HTTP_200_OK)


class MediaRatingViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = MediaRating.objects.all()
    serializer_class = MediaRatingSerializer

    def get_queryset(self):
        media_id = self.request.GET.get('media')
        author_id = self.request.GET.get('author')
        return MediaRating.objects.filter(media_id=media_id, author_id=author_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CustomSearchFilter(SearchFilter):
    search_param = "media"


class MediaSearchAPIView(generics.ListAPIView):
    queryset = Media.objects.all()
    permissions_classes = (permissions.IsAuthenticated,)
    serializer_class = MediaSerializer
    filter_backends = [CustomSearchFilter]
    search_fields = ['title', 'description']


class MediaOrderAPIView(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ('views_count', 'date_posted')
