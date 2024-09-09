from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='statci/course_images/')
    video = models.FileField(upload_to='static/course_videos/',blank=True)

    def __str__(self):
        return self.name
    

class CourseTitle(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, related_name='titles', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class CourseSubtitle(models.Model):
    chapters = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    course = models.CharField(max_length=255)
    course_title = models.ForeignKey(CourseTitle, related_name='chapters', on_delete=models.CASCADE)
    course_name = models.ForeignKey(Course,related_name='course',on_delete=models.CASCADE)

    def __str__(self):
        return self.chapters