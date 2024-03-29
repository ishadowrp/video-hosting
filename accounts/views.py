import json
from rest_framework import viewsets, permissions
from .models import ProfileData, VerificationData, AvatarData
from django.contrib.auth import get_user_model
from .permissions import IsUserOrReadOnly
from .serializers import UserSerializer, ProfileDataSerializer, VerificationPhoneSerializer, AvatarDataSerializer
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .nexmo import check_verification


class VerificationApiView(UpdateAPIView):
    permission_classes = (IsUserOrReadOnly, permissions.IsAuthenticated,)
    serializer_class = VerificationPhoneSerializer

    def patch(self, request):
        serializer = VerificationPhoneSerializer(data=request.data)
        if serializer.is_valid():
            profile = ProfileData.objects.get(username=request.user)
            str_data = json.dumps(request.data)
            data = json.loads(str_data)
            status_verification = check_verification(profile, data)
            if status_verification:
                profile.telephone_verified = True
                profile.save()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsUserOrReadOnly, permissions.IsAuthenticated,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class ProfileDataViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsUserOrReadOnly)
    queryset = ProfileData.objects.all()
    serializer_class = ProfileDataSerializer
    lookup_field = 'username'

    def perform_create(self, serializer):
        serializer.save(id=self.request.user.id, username=self.request.user)


class UserAvatarAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AvatarDataSerializer

    def get(self, request):
        avatar_list = AvatarData.objects.filter(username=self.request.user)
        if len(avatar_list) > 0:
            avatar_data = avatar_list[0]
            serializer = AvatarDataSerializer(avatar_data)
            return Response(serializer.data)
        else:
            return Response()

    def post(self, request):
        serializer = AvatarDataSerializer(data=request.data)
        if serializer.is_valid():
            objs = AvatarData.objects.filter(username=self.request.user)
            if len(objs) > 0:
                for obj in objs:
                    obj.delete()

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        obj = AvatarData.objects.filter(username=request.user)
        obj.delete()
        return Response(status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(username=self.request.user)
