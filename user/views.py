from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.permissions import *

from django.utils import timezone
from django.shortcuts import get_object_or_404

from helpers.randomizer import generate_random_password

from .models import *
from .serializers import *
from helpers.permissions import *

from helpers.otp import OTP_VALID_TIME, generate_otp, is_otp_time_valid


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        first_name = serializer.data.get('first_name')
        last_name = serializer.data.get('last_name')
        role = serializer.data.get('role')

        if first_name and \
                last_name and \
                role:
            user.status = 'verified'
            user.save()
            serializer.data['status'] = 'verified'

        # Generate token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return Response({
            'status': True,
            "message": "Pofile muvaffaqiyatli yangilandi",
            'access': access_token,
            'refresh': refresh_token,
            'user': serializer.data
        })


class GetMeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_serializer = UserSerializer(user)

        # Generate token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        pic = request.build_absolute_uri(user.pic.url)

        user_data = user_serializer.data
        user_data['pic'] = pic
        user_data['id'] = user.id

        return Response({
            'status': True,
            'access': access_token,
            'refresh': refresh_token,
            'user': user_data
        }, status=200)
