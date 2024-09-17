from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model  # Import the custom user model
from .models import UserProgress
from course.models import Course, CourseTitle
from .serializers import UserProgressSerializer

User = get_user_model()

class UserProgressViewSet(viewsets.ViewSet):
    serializer_class = UserProgressSerializer

    def create(self, request):
        user_id = request.data.get('user')
        course_title_id = request.data.get('course_title')

        if not user_id or not course_title_id:
            return Response({"error": "user and course_title are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(id=user_id).exists():
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(id=user_id)
        course_title = get_object_or_404(CourseTitle, id=course_title_id)

        progress, created = UserProgress.objects.get_or_create(
            user=user,
            course_title=course_title
        )

        if not progress.viewed:
            progress.viewed = True
            progress.save()
            return Response({"message": "Progress registered successfully"}, status=status.HTTP_201_CREATED)

        return Response({"message": "Progress already registered"}, status=status.HTTP_200_OK)

    def list(self, request):
        user_id = request.query_params.get('user')

        if not user_id:
            return Response({"error": "user parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(id=user_id).exists():
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(id=user_id)
        progress = UserProgress.objects.filter(user=user)

        total_titles = CourseTitle.objects.count()
        viewed_titles = progress.filter(viewed=True).count()

        if total_titles > 0:
            viewed_percentage = (viewed_titles / total_titles) * 100
        else:
            viewed_percentage = 0

        return Response({
            "total_titles": total_titles,
            "viewed_titles": viewed_titles,
            "viewed_percentage": viewed_percentage
        })

    def retrieve(self, request, pk=None):
        course_id = pk
        user_id = request.query_params.get('user')

        if not user_id or not course_id:
            return Response({"error": "user and course parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(id=user_id).exists():
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(id=user_id)

        try:
            course = Course.objects.get(id=course_id)
            total_titles = CourseTitle.objects.filter(course=course).count()
            user_progress = UserProgress.objects.filter(user=user, course_title__course=course)
            viewed_titles = user_progress.filter(viewed=True).count()

            if total_titles > 0:
                viewed_percentage = (viewed_titles / total_titles) * 100
            else:
                viewed_percentage = 0

            return Response({
                "course": course.name,
                "total_titles": total_titles,
                "viewed_titles": viewed_titles,
                "viewed_percentage": viewed_percentage
            })

        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
