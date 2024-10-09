from rest_framework.serializers import ModelSerializer
from .models import *
class CoursePlaneSerializer(ModelSerializer):
    class Meta:
        model = CoursePlan
        fields = '__all__'