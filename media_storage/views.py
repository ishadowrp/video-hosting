from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from accounts.permissions import IsOwnerOrReadOnly

from .serializers import MediaSerializer, MediaRatingSerializer
from .models import Media, MediaRating
from comments_and_chats.models import Comment


class MediaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated,)
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

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

        list_of_comments = []
        for item in comments:
            dict_message = {'author': item.author.username, 'author_id': item.author.pk,
                            'date_posted': item.date_posted.strftime("%d-%m-%Y %H:%M:%S"), 'content': item.content}
            list_of_comments.append(dict_message)

        dict_response = {'chat': pk, 'title': media.title, 'comments': list_of_comments}

        return Response(dict_response)


class MediaRatingViewSet(viewsets.ModelViewSet):
    queryset = MediaRating.objects.all()
    serializer_class = MediaRatingSerializer
