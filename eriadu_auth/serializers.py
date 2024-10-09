# myapp/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from course.models import Course
from course.serializers import CourseSerializer
from payment.models import Factor
from .models import UserCourse
CustomUser = get_user_model()

class CustomUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','user_phone']            
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required':False
                },
            'username':{'required':False},              
            'email':{'required':False},              
            }



class OTPVerifySerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)



class UserCourseAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def get_accessible_courses(self, user):
        # Return all courses if the user is pro
        if user.is_pro:
            return Course.objects.all()

        # Otherwise, return only courses assigned to the user
        return user.courses.all()
    



class CustomUserCourseSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ['user_phone','courses']
        def get_accessible_courses(self, user):
            if user.is_pro:
                return Course.objects.all()
            return user.courses.all()
        
        def update(self, instance, validated_data):
            courses = validated_data.pop('courses', [])
            instance = super().update(instance, validated_data)
            if courses:
                instance.courses.set(courses)
            return instance


class UserFactorDetails(serializers.ModelSerializer):
    class Meta:
        model = Factor
        fields = '__all__'

class CustomCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','name','is_pro','description', 'image']

class UserCourseSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())  # فقط شناسه دوره از کلاینت دریافت شود

    class Meta:
        model = UserCourse
        fields = ('id', 'user', 'course')  # user را فقط برای نمایش استفاده می‌کنیم
        read_only_fields = ('user',)  # کاربر به‌صورت خودکار تنظیم می‌شود