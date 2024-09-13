from rest_framework import serializers
from .models import Course, CourseTitle,CourseSubtitle

class AddCourseTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTitle
        fields = ['course', 'title']


class CourseSubtitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubtitle
        fields = ['course_name','course_title','content','chapters']


class CourseTitleSerializer(serializers.ModelSerializer):
    chapters = CourseSubtitleSerializer(many=True, read_only=True)
    class Meta:
        model = CourseTitle
        fields = ['id', 'title', 'chapters']


class CourseSerializer(serializers.ModelSerializer):
    titles = CourseTitleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'is_pro','description' , 'image', 'video', 'titles']



class CourseChapterSerializer(serializers.ModelSerializer):
    course_title = serializers.PrimaryKeyRelatedField(queryset=CourseTitle.objects.all())

    class Meta:
        model = CourseSubtitle
        fields = ['id', 'chapters', 'content', 'course_title']


class CourseSubtitleCreateSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=True)
    course_title = serializers.PrimaryKeyRelatedField(queryset=CourseTitle.objects.all(), required=True)

    class Meta:
        model = CourseSubtitle
        fields = ['course', 'course_title', 'chapters', 'content']

    def validate(self, data):
        course = data.get('course')
        course_title = data.get('course_title')

        # بررسی اینکه course_title به course مربوط است یا خیر
        if course_title.course != course:
            raise serializers.ValidationError("عنوان انتخاب شده به دوره انتخاب شده تعلق ندارد.")
        return data
    


