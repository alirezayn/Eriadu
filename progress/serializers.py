# progress/serializers.py
from rest_framework import serializers
from progress.models import UserProgress

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['user','course', 'current_section', 'completed_sections', 'answered_questions', 'progress_percentage', 'last_accessed']