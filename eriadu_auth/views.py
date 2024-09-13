# myapp/views.py
from rest_framework.response import Response
from rest_framework import generics, permissions,viewsets,status
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny,IsAuthenticated
from course.models import Course
from course.serializers import CourseSerializer
from .serializers import CustomUserSerializer,OTPVerifySerializer,UserCourseAccessSerializer
from .models import CustomUser,OTP
from .permission import *
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import pyotp
import random
from rest_framework_simplejwt.tokens import RefreshToken

user = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['user_phone'] = user.user_phone
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token

class CreateUserView(generics.CreateAPIView):
    model = user
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        # فراخوانی سریالایزر برای تایید داده‌ها
        phone = request.data.get('user_phone')
        user_exists = user.objects.filter(user_phone=phone).first()
    
        if user_exists:
            otp_code = str(random.randint(100000, 999999))
            otp_object = OTP.objects.create(user_id=user_exists.id,otp_code=otp_code)
            return Response({
                'suceess':True,
                'message': 'New OTP has been generated and sent to the user.',
                'otp_code': otp_object.otp_code,  # This should be sent through a secure channel in a real application
                'otp_required': True,
            }, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ذخیره کاربر و غیر فعال کردن حساب کاربری
        user_instance = serializer.save(is_staff=False, is_superuser=False, is_active=False)

        # تولید OTP
        otp_code = str(random.randint(100000, 999999))  # تولید یک کد ۶ رقمی
        OTP.objects.create(user=user_instance, otp_code=otp_code)

        # ارسال OTP به شماره تلفن (مثلاً پیامک یا سیستم دیگری)
        user_phone = serializer.validated_data.get('user_phone')




        # ایجاد پاسخ سفارشی
        return Response({
            'success':True,
            'otp_code': otp_code,
            'message': 'User created, please verify OTP',
            'user_phone': user_phone
        }, status=status.HTTP_201_CREATED)

class VerifyOTPView(generics.GenericAPIView):
    serializer_class = OTPVerifySerializer

    def post(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        otp_code = request.data.get('otp_code')
        
        otp = get_object_or_404(OTP, otp_code=otp_code)
        
        # بررسی صحت و اعتبار OTP
        if otp:
            # فعال کردن کاربر
            user = otp.user
  
            user.is_active = True
            user.save()
            refresh = user.get_token()
            otp.delete()
            return Response({'success': True,'access':str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)



class CreateAdminUserView(generics.CreateAPIView):
    model = user
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        serializer.save(is_staff=True, is_superuser=True)




class ShowUserViewSet(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = [IsAuthenticated]
    # def get_queryset(self):
    #     user = self.request.user

    #     if user.is_pro:
    #         # Return all courses if user is pro
    #         return CustomUser.objects.all()
        
    #     else:
    #         # Return only courses assigned to the user
    #         return CustomUser.courses.filter(id=user.id)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('user_phone')
        auth_user = user.objects.filter(user_phone=phone_number).first()

        if auth_user:
            refresh = RefreshToken.for_user(auth_user)
            # Generate and send OTP
            new_otp_code = str(random.randint(100000, 999999))
            otp_object = OTP.objects.filter(user_id=auth_user.id).first()
            otp_object.otp_code = new_otp_code
            otp_object.save()
            # Return the OTP for verification (for testing purposes)
            return Response({
                'message': 'New OTP has been generated and sent to the user.',
                'otp_code': otp_object.otp_code,  # This should be sent through a secure channel in a real application
                'otp_required': True,
            }, status=status.HTTP_200_OK)

        return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)



class UserCourseModelViewSet(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = UserCourseAccessSerializer



class AccessibleCourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.is_pro:
            # Pro users can access all courses
            return Course.objects.all()
        else:
            # Return only the courses assigned to the user
            return user.courses.all()