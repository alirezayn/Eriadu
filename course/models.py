from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='static/course_images/')
    video = models.FileField(upload_to='static/course_videos/',blank=True)
    is_pro = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    

class CourseTitle(models.Model):
    chapter = models.CharField(max_length=255,blank=False,null=False)
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
    code = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    sound = models.FileField(upload_to='static/SubSectionContent/sounds/',null=True,blank=True)
    sub_section_content = models.ForeignKey(SubSection,related_name='sub_section_content',on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['priority']  




class CourseIntroduction(models.Model):
    headline = models.CharField(max_length=500)  # تیتر اصلی
    description = models.TextField()  # توضیحات کامل محصول یا دوره
    image = models.ImageField(upload_to='static/course_intro/', null=True, blank=True)  # تصویر معرفی
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ایجاد
    updated_at = models.DateTimeField(auto_now=True)  # تاریخ به‌روزرسانی
    course_intro = models.ForeignKey(Course,related_name='course_intro',on_delete=models.CASCADE)

    def __str__(self):
        return self.headline
    


class CourseExam(models.Model):
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
    exam = models.ForeignKey(Course,related_name='exam',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title



class CourseInteraction(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    interaction_type = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)



class TitleInteraction(models.Model):
    title = models.ForeignKey(CourseTitle,on_delete=models.CASCADE,related_name='title_interaction')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    locked = models.BooleanField(default=True)