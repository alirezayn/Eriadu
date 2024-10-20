from rest_framework.serializers import ModelSerializer,SerializerMethodField
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


class UserActivitySerializer(ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['id','total','course']
        depth = 1


class UserCourseSerializer(ModelSerializer):
    user_activity = SerializerMethodField()  # Use SerializerMethodField for custom logic

    class Meta:
        model = UserCourse
        fields = ['course', 'user_activity']  # Include the fields you want

    def get_user_activity(self, obj):
        # Replace this logic with whatever makes sense for retrieving the user activity
        user = self.context['request'].user  # Get the current user from the request context
        # Fetch UserActivity for the user, or implement your logic here
        user_activity = UserActivity.objects.filter(user=user).first()  # Adjust according to your logic
        
        if user_activity:
            return UserActivitySerializer(user_activity).data
        return None  # Return None if no UserActivity is found

class UserSearchSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','user_phone']




