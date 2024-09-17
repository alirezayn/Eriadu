from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView,RetrieveAPIView,DestroyAPIView
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from .models import Course, CourseExam, CourseIntroduction, CourseTitle, CourseSubtitle,QuestionTitleSection, SubSection, SubSectionContent
from .serializers import (
    CourseExamSerializer,
    CourseIntroSerializer,
    CourseSerializer,
    CourseTitleSerializer,
    CourseSubtitleSerializer,
    AddCourseTitleSerializer,
    CourseNameSerializer,
    CourseNameSerializerById,
    CourseTitleSectionSerializer,
    ExamSerializer,QuestioSectionSerialzer,
    SubSectionContentSerializer,SubSectionSerializer,CourseIntroductionSerializer
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


class SectionTitleViewSet(RetrieveAPIView,DestroyAPIView):
    serializer_class = CourseTitleSectionSerializer
    lookup_field = 'id'
    def get_object(self):
        request: Request = self.request
        query = request.query_params.get('id')
        if query:
            try:
                return CourseTitle.objects.get(id=query)
            except CourseTitle.DoesNotExist:
                raise NotFound("CourseTitle with this ID does not exist.")
        else:
            raise NotFound("ID parameter is required.")

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "section deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



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
        request : Request = self.request
        course_id = request.query_params.get('id')
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



class CourseIntroductionViewSet(viewsets.ModelViewSet):
    queryset = CourseIntroduction.objects.all()
    serializer_class = CourseIntroSerializer


class CourseIntroViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseIntroductionSerializer
    


class ExamViewSet(viewsets.ModelViewSet):
    queryset = CourseExam.objects.all()
    serializer_class = ExamSerializer


class CourseExamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseExamSerializer