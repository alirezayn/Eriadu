from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from .models import Course, CourseTitle, CourseSubtitle
from .serializers import (
    CourseSerializer,
    CourseTitleSerializer,
    CourseSubtitleSerializer,
    AddCourseTitleSerializer,
    CourseNameSerializer
)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer



class CourseTitleViewSet(viewsets.ModelViewSet):
    queryset = CourseTitle.objects.all()
    serializer_class = AddCourseTitleSerializer


class CourseSubtitleCreateSerializer(viewsets.ModelViewSet):
    queryset = CourseSubtitle.objects.all()
    serializer_class = CourseSubtitleSerializer



class CourseNameListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseNameSerializer
