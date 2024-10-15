from rest_framework.serializers import ModelSerializer
from payment.models import *
from course.models import *
from progress.models import *
from eriadu_auth.models import *

class FactorReportSerializer(ModelSerializer):
    class Meta:
        model = Factor
        fields = '__all__'


class PlanSerializer(ModelSerializer):
    class Meta:
        model = CoursePlan
        field = '__all__'


class FactorReportDetailSerilizer(ModelSerializer):
    class Meta:
        model = Factor
        fields = '__all__'
        depth = 1  # مقدار 1 یعنی روابط مستقیم سریالایز شوند


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        depth = 2

class UserSearchSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','user_phone']




