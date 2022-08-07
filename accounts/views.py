import json
from rest_framework import viewsets, permissions
from .models import ProfileData, VerificationData
from django.contrib.auth import get_user_model
from .permissions import IsUserOrReadOnly
from .serializers import UserSerializer, ProfileDataSerializer, VerificationPhoneSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from nexmo import check_verification


class VerificationTelephoneCheck(APIView):
    permission_classes = (IsUserOrReadOnly, permissions.IsAuthenticated,)

    @staticmethod
    def patch(request):
        serializer = VerificationPhoneSerializer(data=request.data)
        if serializer.is_valid():
            profile = ProfileData.objects.get(username=request.user)
            str_data = json.dumps(request.data)
            data = json.loads(str_data)
            status_verification = check_verification(profile, data)
            if status_verification:
                profile.telephone_verified = True
                profile.save()
                verification = VerificationData.get(profile=profile)
                verification.delete()  # Почистил отработанную информацию
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
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ProfileData.objects.all()
    serializer_class = ProfileDataSerializer
    lookup_field = 'username'


class UserAvatarAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsUserOrReadOnly)
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProfileDataSerializer

    @staticmethod  # Проверить работает ли со статик методом
    def post(request):
        serializer = ProfileDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod  # Проверить работает ли со статик методом
    def delete(request):
        obj = ProfileData.objects.filter(username=request.user)
        obj.avatar.delete()

    def perform_create(self, serializer):
        serializer.save(username=self.request.user)
