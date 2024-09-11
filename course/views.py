from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework.decorators import action
from .models import Course, CourseTitle, CourseSubtitle
from .serializers import (
    CourseSerializer,
    CourseTitleSerializer,
    CourseSubtitleSerializer,
    AddCourseTitleSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=["get"])
    def filter_by(self, request: Request, pk=None):
        course_name = request.query_params.get("course_name")
        print(course_name)
        if course_name:
            result = CourseTitle.objects.filter(name=course_name)

            serializer = CourseTitleSerializer(result, many=True)
            return Response(
                {"result": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"result": False, "error": "course_name params must be set"}
            )


class CourseTitleViewSet(viewsets.ModelViewSet):
    queryset = CourseTitle.objects.all()
    serializer_class = AddCourseTitleSerializer


class CourseSubtitleCreateSerializer(viewsets.ModelViewSet):
    queryset = CourseSubtitle.objects.all()
    serializer_class = CourseSubtitleSerializer
