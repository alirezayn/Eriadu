from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.decorators import action
from .models import Course, CourseTitle, CourseSubtitle,QuestionTitleSection, SubSection, SubSectionContent
from .serializers import (
    CourseSerializer,
    CourseTitleSerializer,
    CourseSubtitleSerializer,
    AddCourseTitleSerializer,
    CourseNameSerializer,
    CourseNameSerializerById,
    CourseTitleSectionSerializer,QuestioSectionSerialzer,
    SubSectionContentSerializer,SubSectionSerializer
)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['post'])
    def title(self, request:Request, pk=None):
        query = request.query_params.get('title')
        print(query)


class CourseTitleViewSet(viewsets.ModelViewSet):
    queryset = CourseTitle.objects.all()
    serializer_class = AddCourseTitleSerializer


class SectionTitleViewSet(ListAPIView):
    serializer_class = CourseTitleSectionSerializer
    def get_queryset(self):
        request :Request = self.request
        query = request.query_params.get('id')
        print(query)
        if query:
            return CourseTitle.objects.filter(id=query)
        else:
            return CourseTitle.objects.none()


class CourseSubtitleCreateViewSet(viewsets.ModelViewSet):
    queryset = CourseSubtitle.objects.all()
    serializer_class = CourseSubtitleSerializer



class CourseNameListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseNameSerializer



class CourseNameListViewById(RetrieveAPIView):
    serializer_class =CourseNameSerializerById
    lookup_field = 'id'

    def get_object(self):
        course_id = self.request.query_params.get('id')
        return get_object_or_404(Course, id=course_id)

class QuestionSectionViewSet(viewsets.ModelViewSet):
    queryset = QuestionTitleSection.objects.all()
    serializer_class = QuestioSectionSerialzer


class SubSectionViewSet(viewsets.ModelViewSet):
    queryset = SubSection.objects.all()
    serializer_class = SubSectionSerializer

class SubSectionContentViewSet(viewsets.ModelViewSet):
    queryset = SubSectionContent.objects.all()
    serializer_class = SubSectionContentSerializer
