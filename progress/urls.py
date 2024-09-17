# progress/urls.py
from django.urls import path
from .views import * 

urlpatterns = [
    path('', UserProgressListView.as_view(), name='user-progress-list'),
    path('course/<int:course_id>/', UserProgressDetailView.as_view(), name='user-progress-detail'),
    path('complete-section/<int:course_id>/<int:section_id>/', CompleteSectionView.as_view(), name='complete-section'),
    path('complete-title/<int:course_id>/<int:title_id>/', CompleteTitleView.as_view(), name='complete-title'),
]