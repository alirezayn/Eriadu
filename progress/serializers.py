# from rest_framework import serializers
# from .models import UserProgress

# class UserProgressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProgress
#         fields = ['id','user', 'course_title','completed','progress_percentage']

from rest_framework import serializers
from .models import UserProgress

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['user', 'course_title', 'viewed']
