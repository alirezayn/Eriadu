from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'list', CourseViewSet)
router.register(r'titles', CourseTitleViewSet)
router.register(r'chapters', CourseSubtitleCreateViewSet)
router.register(r'question',QuestionSectionViewSet)
router.register(r'Exam',ExamViewSet)
router.register(r'ExamList',CourseExamViewSet,basename='ExamList')
router.register(r'sub_section',SubSectionViewSet)
router.register(r'sub_section_content',SubSectionContentViewSet)
router.register(r'course-introductions', CourseIntroductionViewSet)
router.register('intro',CourseIntroViewSet,basename='intro')


urlpatterns = [
    path('', include(router.urls)),
    path('category/',view=CourseNameListView.as_view(),name='course_list'),
    path('category_by_id/',view=CourseNameListViewById.as_view(),name='course_by_id'),
    path('section/',view=SectionTitleViewSet.as_view(),name='section'),
    path('question_list/',view=TitleQuestionListView.as_view(),name='question_list'),
    path('viewed/<int:course_id>/',view=RegisterView.as_view(),name='viewed'),
    path('viewed/trending/', TrendingCourseS.as_view(), name='trending-courses'),

]



