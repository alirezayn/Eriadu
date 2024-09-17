# # progress/models.py
# from django.db import models
# from django.conf import settings
# from course.models import Course, CourseSubtitle, QuestionTitleSection,CourseTitle

# class UserProgress(models.Model):

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
#     course_title = models.ForeignKey(CourseTitle, related_name='user_progress', on_delete=models.CASCADE)
#     completed_titles = models.ManyToManyField(CourseTitle, related_name='completed_titles', blank=True)  # Add this line
#     completed = models.BooleanField(default=False)
#     progress_percentage = models.FloatField(default=0)

#     def __str__(self):
#         return f'{self.user.user_phone} - {self.course_title.chapter} Progress'


from django.conf import settings
from django.db import models
from course.models import CourseTitle

class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    course_title = models.ForeignKey(CourseTitle, related_name='user_progress', on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.course_title.chapter}'
