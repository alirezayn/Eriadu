# myapp/views.py
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics, permissions,viewsets,status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny,IsAuthenticated
from course.models import Course
from course.serializers import CourseSerializer
from .serializers import *
from .models import CustomUser,OTP
from .permission import *
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import pyotp
import random
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import send_verification_code

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



class LoginPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


<<<<<<< HEAD




=======
>>>>>>> 96c457ef78fec5f13d4dde6cee8534de9330bd51
class CreateUserView(generics.CreateAPIView):
    model = user
    serializer_class = CustomUserRegisterSerializer

    def create(self, request, *args, **kwargs):
        phone = request.data.get('user_phone')
        user_exists = user.objects.filter(user_phone=phone).first()

        if user_exists:
            former_otp = OTP.objects.filter(user_id=user_exists.id)
            former_otp.delete()
            otp_code = str(random.randint(100000, 999999))
            otp_object = OTP.objects.create(user_id=user_exists.id,otp_code=otp_code)
            # send_verification_code(phone,str(otp_object.otp_code))

            return Response({
                'success':True,
                'message': 'New OTP has been generated and sent to the user.',
                'otp_code': otp_object.otp_code,
                'otp_required': True,
            }, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        user_instance = serializer.save(is_staff=False, is_superuser=False, is_active=False)


        otp_code = str(random.randint(100000, 999999))
        OTP.objects.create(user=user_instance, otp_code=otp_code)


        user_phone = serializer.validated_data.get('user_phone')

        # send_verification_code(user_phone,str(otp_code))



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

        otp_code = request.data.get('otp_code')

        otp = get_object_or_404(OTP, otp_code=otp_code)

        if otp:
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
    serializer_class = CustomUserRegisterSerializer

    def perform_create(self, serializer):
        serializer.save(is_staff=True, is_superuser=True)


class ShowUserViewSet(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = CustomUserRegisterSerializer


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


class UserCourseListApiView(generics.ListCreateAPIView):
    serializer_class = CustomUserCourseSerializer

    def get_queryset(self):
        user_phone = self.request.query_params.get('phone')
        user_object = user.objects.filter(user_phone=user_phone)
        if user_object:
            return user_object
        else:
            return user.objects.all()


    def patch(self, request, *args, **kwargs):
        user_phone = self.request.data.get('user_phone')
        courses = request.data.get('courses', [])

        try:
            user = CustomUser.objects.get(user_phone=user_phone)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(courses=courses)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class AllUserFactorDetails(viewsets.ModelViewSet):
    queryset = Factor.objects.all()
    serializer_class = UserFactorDetails




class UserCourseListCreateView(generics.ListCreateAPIView):
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # برگرداندن دوره‌های کاربری که وارد سیستم شده
            return UserCourse.objects.filter(user=user)
        else:
            return UserCourse.objects.none()

    def perform_create(self, serializer):
        try:
            user_phone = self.request.user.user_phone
            custom_user = CustomUser.objects.get(user_phone=user_phone)
            serializer.save(user=custom_user)
            # پس از ذخیره‌سازی موفق، پیام موفقیت برگردانده می‌شود
            self.response_message = {"message": True}
        except:
        #     # اگر خطایی رخ دهد، پیام خطا برگردانده می‌شود
            self.response_message = {"message": False}

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # در اینجا تنها پیام را به جای داده‌های دیگر برمی‌گردانیم
        return Response(self.response_message, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": False}, status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)


class RetrieveUserCourseAPI(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            # فیلتر کردن رکوردها بر اساس کاربر احراز هویت شده
            queryset = UserCourse.objects.filter(user=user)
            serializer = UserCourseSerializer(queryset, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
