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

class SendCodeAPIView(APIView):
    http_method_names = ['post']
    """
        Algorithm to send OTP to user's telegram
        1. Generate OTP
        2. Send OTP to user's telegeam
        3. Store OTP in database for verification
    """
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        role = request.data.get('role', None)
        
        user = User.objects.filter(username=user_id).first()

        if (user):
            code_create_at = user.code_creation_time

            if is_otp_time_valid(code_create_at):
                return Response({
                    'message':"Sizning tasdiqlash kodingiz hali eskirmagan",
                    'data': {
                        'redirect_url': f'?code={user.code}&id={user.username}&lang={user.lang}',
                    }
                }, status=302)

            user.code = generate_otp()
            user.code_creation_time = timezone.now()
            user.is_active = False
            user.save()

            return Response({
                'message':"Sizning tasdiqlash kodingiz yangilandi.",
                'data': {
                    'redirect_url': f'?code={user.code}&id={user.username}&lang={user.lang}',
                }
            }, status=200)

        otp = generate_otp()
        random_password = generate_random_password(length=8)

        if not role:
            return Response({
                'message':"Iltimos, role kiritib ko'ring",
            }, status=400)
        
        user = User.objects.create_user(
            username=user_id,
            password=random_password,
            code_creation_time = timezone.now(),
            code=otp
        )
        
        user.is_active = False
        user.status = 'unconfirmed'
        user.role = role
        user.save()
        
        return Response({
            'message':f"Siznga tasdiqlash kodingiz yuborildi. Kodning {OTP_VALID_TIME} daqiqadan so'ng eskiradi ",
            'data': {
                'redirect_url': f'?code={user.code}&id={user.username}&lang={user.lang}',
            }
        }, status=201)

class ConfirmCodeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        code = request.data.get('code', None)

        if not user_id or \
            not code:
            return Response({
                'message':"Iltimos, user_id va code kiritib ko'ring",
            })
        
        user = get_object_or_404(User, username=user_id)
        code_create_at = user.code_creation_time
        serializer = UserSerializer(user)
        
        if user.code == int(code):
            if not is_otp_time_valid(code_create_at):
                return Response({
                    'status': False,
                    'message':"Kodni amal qilish muddati tugagan. Iltimos, qayta urunib ko'ring",
                }, status=400)
        
            user.is_active = True
            user.status = 'confirmed'
            user.save()
            
            # Generate token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            if user.pic:
                pic = request.build_absolute_uri(user.pic.url)
            else:
                pic = None
            
            user_data = serializer.data
            user_data['pic'] = pic
            user_data['id'] = user.id
            
            return Response({
                'status':True,
                'message':"Kod tasdiqlandi",
                'access': access_token,
                'refresh': refresh_token,
                'user': user_data
            }, status=200)
            
        return Response({
            'status':False,
            'message':"Tasdiqlash kodingiz xato. Iltimos, qayta urunib ko'ring",
        }, status=400)


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class =  UserSerializer
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
            'status':True,
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
                'status':True,
                'access': access_token,
                'refresh': refresh_token,
                'user': user_data
            }, status=200)

