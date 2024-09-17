# progress/views.py
from rest_framework import generics
from progress.models import UserProgress
from .serializers import UserProgressSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from course.models import Course, CourseSubtitle, QuestionTitleSection
from .utils import complete_section, answer_question



class CompleteSectionView(APIView):
    def post(self, request, course_id, section_id):
        user = request.user
        
        # Try to get the Course and CourseSubtitle objects
        try:
            course = Course.objects.get(id=course_id)
            section = CourseSubtitle.objects.get(id=section_id)
        except (Course.DoesNotExist, CourseSubtitle.DoesNotExist):
            return Response({'message': False}, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark the section as complete for the user
        complete_section(user, course, section)
        
        return Response({'message': True}, status=status.HTTP_200_OK)
class AnswerQuestionView(APIView):
    def post(self, request, course_id, question_id):
        user = request.user
        section = Course.objects.get(id=course_id)
        question = QuestionTitleSection.objects.get(id=question_id)

        # ثبت پاسخ کاربر برای سکشن مشخص
        answer_question(user, section, question)

        return Response({'message': True}, status=status.HTTP_200_OK)
            

class UserProgressListView(generics.ListAPIView):
    serializer_class = UserProgressSerializer
    queryset = UserProgress.objects.all()
 


class UserProgressDetailView(generics.RetrieveAPIView):
    serializer_class = UserProgressSerializer
    lookup_field = 'course_id'

    def get_queryset(self):
        user = self.request.user
        return UserProgress.objects.filter(user=user)
