from rest_framework import viewsets
from .models import Course,CourseTitle,CourseSubtitle
from .serializers import CourseSerializer,CourseTitleSerializer,CourseSubtitleSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer



class CourseTitleViewSet(viewsets.ModelViewSet):
    queryset = CourseTitle.objects.all()
    serializer_class = CourseTitleSerializer


class CourseSubtitleCreateSerializer(viewsets.ModelViewSet):
    queryset = CourseSubtitle.objects.all()
    serializer_class = CourseSubtitleSerializer


