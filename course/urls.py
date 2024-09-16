from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'list', CourseViewSet)
router.register(r'titles', CourseTitleViewSet)
router.register(r'chapters', CourseSubtitleCreateViewSet)
router.register('question',QuestionSectionViewSet)
router.register('sub_section',SubSectionViewSet)
router.register('sub_section_content',SubSectionContentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('category/',view=CourseNameListView.as_view(),name='course_list'),
    path('category_by_id/',view=CourseNameListViewById.as_view(),name='course_by_id'),
    path('section/',view=SectionTitleViewSet.as_view(),name='section')
]