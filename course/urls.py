from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet,CourseTitleViewSet,CourseSubtitleCreateSerializer

router = DefaultRouter()
router.register(r'list', CourseViewSet)
router.register(r'titles', CourseTitleViewSet)
router.register(r'chapters', CourseSubtitleCreateSerializer)

urlpatterns = [
    path('', include(router.urls)),
]