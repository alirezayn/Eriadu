# myapp/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from course.models import Course
from course.serializers import CourseSerializer
CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)  # Include accessible courses


    class Meta:
        model = CustomUser
        # fields = ('id', 'username','email', 'first_name', 'last_name','user_phone', 'password','is_staff','is_active','is_superuser')
        # fields = '__all__'
        fields = ['user_phone']            
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required':False
                },
            'username':{'required':False},              
            'email':{'required':False},              
            }
        def get_accessible_courses(self, user):
        # Return all courses if the user is pro
            if user.is_pro:
                return Course.objects.all()

            # Otherwise, return only courses assigned to the user
            return user.courses.all()

    # def create(self, validated_data):
    #     user = CustomUser.objects.create_user(
    #         # username=validated_data["username"],
    #         # email=validated_data['email'],
    #         # password=validated_data['password'],
    #         # first_name=validated_data.get('first_name', ''),
    #         # last_name=validated_data.get('last_name', ''),
    #         # is_active = validated_data['is_active'],
    #         # is_staff = validated_data['is_staff'],
    #         # is_superuser = validated_data['is_superuser'],
    #         user_phone = validated_data['user_phone']

    #     )        
    #     return user
    
    # def update(self, instance, validated_data):
    #     password = validated_data.get('password', None)
    #     if password:
    #         validated_data['password'] = make_password(password)
    #     return super().update(instance, validated_data)
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