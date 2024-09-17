# progress/models.py
from django.db import models
from django.conf import settings
from course.models import Course, CourseSubtitle, QuestionTitleSection,CourseTitle

class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress_users')
    current_section = models.ForeignKey(CourseSubtitle, on_delete=models.SET_NULL, null=True, blank=True)
    course_title = models.ForeignKey(CourseTitle,on_delete=models.SET_NULL,null=True,blank=True)
    completed_title = models.ManyToManyField(CourseTitle,related_name='completed_title',blank=True)
    completed_sections = models.ManyToManyField(CourseSubtitle, related_name='completed_by_users', blank=True)
    answered_questions = models.ManyToManyField(QuestionTitleSection, related_name='answered_by_users', blank=True)
    progress_percentage = models.FloatField(default=0.0)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"

    def update_progress(self):
        """Custom method to update progress based on completed sections and titles."""
        total_titles = self.course.titles.count()  # Total course titles
        total_sections = self.course.titles.aggregate(
            total_sections=models.Count('subtitles')
        )['total_sections']  # Total sections across all titles
        
        completed_titles_count = self.completed_title.count()  # Completed titles
        completed_sections_count = self.completed_sections.count()  # Completed sections
        
        if total_titles > 0:
            # Calculate progress based on both titles and sections
            title_progress = (completed_titles_count / total_titles) * 50  # Titles contribute 50% to progress
        else:
            title_progress = 0
        
        if total_sections > 0:
            section_progress = (completed_sections_count / total_sections) * 50  # Sections contribute 50% to progress
        else:
            section_progress = 0

        # Overall progress is the sum of title and section progress
        self.progress_percentage = title_progress + section_progress
        self.save()