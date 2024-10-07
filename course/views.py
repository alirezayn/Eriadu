from django.utils import timezone
from datetime import  timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView,RetrieveAPIView,DestroyAPIView
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.views import APIView
from .models import Course, CourseExam, CourseInteraction, CourseIntroduction, CourseTitle, CourseSubtitle,QuestionTitleSection, SubSection, SubSectionContent
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
    ExamSerializer,QuestioSectionSerialzer,CourseTitleQuestionSerializer,
    SubSectionContentSerializer,SubSectionSerializer,CourseIntroductionSerializer
)
import subprocess
from rest_framework.decorators import api_view

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
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
    serializer_class = CourseNameSerializerById
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



class TitleQuestionListView(RetrieveAPIView):
    # queryset = CourseTitle.objects.all()
    serializer_class = CourseTitleQuestionSerializer

    def get_object(self):
        request: Request = self.request
        title_id = request.query_params.get('id')

        if not title_id:
            raise NotFound(detail="Title ID is required")

        try:
            return CourseTitle.objects.get(id=title_id)
        except CourseTitle.DoesNotExist:
            raise NotFound(detail="CourseTitle not found")



class RegisterView(APIView):
    def post(self, request:Request, course_id):
        course = Course.objects.get(id=course_id)
        if request.auth:
            # بررسی اینکه آیا این کاربر قبلاً با این کورس تعامل داشته یا نه
            existing_interaction = CourseInteraction.objects.filter(
                course=course,
                user=request.user
            ).exists()

            if existing_interaction:
                return Response({"message": False}, status=status.HTTP_400_BAD_REQUEST)

            # اگر تعامل تکراری نباشد، آن را ثبت می‌کنیم
            interaction = CourseInteraction.objects.create(
                course=course,
                user=request.user,
                interaction_type=True,  # همیشه مقدار True ثبت می‌شود
            )
            
            return Response({"message": True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"user not exists"},status=status.HTTP_401_UNAUTHORIZED)
    

class TrendingCourses(APIView):
    def get(self, request:Request):
        interaction = CourseInteraction.objects.all().count()
        print(interaction)
        return Response({
            "count": str(interaction)
        })

class TrendingCourseS(APIView):
    def get(self, request):
        # بازه زمانی هفت روزه اخیر
        last_week = timezone.now() - timedelta(days=7)

        # محاسبه تعداد تعاملات (interactions) مرتبط با هر کورس
        trending_courses = Course.objects.filter(
            interactions__timestamp__gte=last_week
        ).annotate(
            total_interactions=Count('interactions')
        ).order_by('-total_interactions')[:10]  # نمایش 10 کورس برتر

        # لیست نهایی داده‌های قابل سریالایز
        data = [
            {
                "id": str(course.id),
                "name":str(course.name),
                "image":str(course.image),
                "viewd": str(course.total_interactions)
            }
            for course in trending_courses
        ]

        return Response(data)