from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='static/course_images/')
    video = models.FileField(upload_to='static/course_videos/',blank=True)
    is_pro = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    

class CourseTitle(models.Model):
    chapter = models.CharField(max_length=255)
    course = models.ForeignKey(Course, related_name='titles', on_delete=models.CASCADE)

    def __str__(self):
        return self.chapter


class CourseSubtitle(models.Model):
    section = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    course = models.CharField(max_length=255)
    code = models.TextField(blank=True)
    course_title = models.ForeignKey(CourseTitle, related_name='section', on_delete=models.CASCADE)
    course_name = models.ForeignKey(Course,related_name='course',on_delete=models.CASCADE)

    def __str__(self):
        return self.section
    


class QuestionTitleSection(models.Model):
    title = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    
    ANSWER_CHOICES = (
        ('option_1', 'Option 1'),
        ('option_2', 'Option 2'),
        ('option_3', 'Option 3'),
        ('option_4', 'Option 4'),
    )
    
    answer = models.CharField(max_length=10, choices=ANSWER_CHOICES)
    question = models.ForeignKey(CourseTitle,related_name='question',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    





class SubSection(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='static/subSection/',blank=True,null=True)
    sub_section = models.ForeignKey(CourseSubtitle,related_name='sub_section',on_delete=models.CASCADE)



    def __str__(self) -> str:
        return self.title


class SubSectionContent(models.Model):
    content = models.TextField()
    sub_section_content = models.ForeignKey(SubSection,related_name='sub_section_content',on_delete=models.CASCADE)

    