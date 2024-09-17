# # progress/urls.py
# from django.urls import path
# from .views import * 

# urlpatterns = [
#     path('', UserProgressListView.as_view(), name='user-progress-list'),
#     path('course/<int:course_id>/', UserProgressDetailView.as_view(), name='user-progress-detail'),
#     path('complete-section/<int:course_id>/<int:section_id>/', CompleteSectionView.as_view(), name='complete-section'),
#     path('complete-title/<int:course_id>/<int:title_id>/', CompleteTitleView.as_view(), name='complete-title'),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  UserProgressViewSet

# ایجاد یک router برای ثبت خودکار مسیرهای ViewSet
router = DefaultRouter()
router.register(r'user-progress', UserProgressViewSet, basename='user-progress')

urlpatterns = [
    path('', include(router.urls)),  # این خط مسیرهای ViewSet را شامل می‌شود
    # path('course-progress/<int:course_id>/<int:user_id>/', CourseProgressView.as_view(), name='course-progress'),
    # path('completed-titles/<int:user_id>/', CompletedTitlesView.as_view(), name='completed-titles'),
]
