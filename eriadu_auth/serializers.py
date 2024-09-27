# myapp/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from course.models import Course
from course.serializers import CourseSerializer
from payment.models import Factor
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


class UserFactorDetails (serializers.ModelSerializer):
    class Meta:
        model = Factor
        fields = '__all__'