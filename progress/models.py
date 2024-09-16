# progress/models.py
from django.db import models
from django.conf import settings
from course.models import Course, CourseSubtitle, QuestionTitleSection

class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress_users')
    current_section = models.ForeignKey(CourseSubtitle, on_delete=models.SET_NULL, null=True, blank=True)
    completed_sections = models.ManyToManyField(CourseSubtitle, related_name='completed_by_users', blank=True)
    answered_questions = models.ManyToManyField(QuestionTitleSection, related_name='answered_by_users', blank=True)
    progress_percentage = models.FloatField(default=0.0)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"

    def update_progress(self):
        """Custom method to update progress based on completed sections."""
        total_sections = self.course.titles.count()
        completed_count = self.completed_sections.count()
        if total_sections > 0:
            self.progress_percentage = (completed_count / total_sections) * 100
        self.save()