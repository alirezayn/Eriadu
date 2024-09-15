from rest_framework import serializers
from .models import Course, CourseTitle,CourseSubtitle

class AddCourseTitleSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(slug_field='name', queryset=Course.objects.all())
    chapter = serializers.CharField()
    class Meta:
        model = CourseTitle
        fields = ['id','course', 'chapter']


class CourseSubtitleSerializer(serializers.ModelSerializer):
    # course_name = serializers.SerializerMethodField()
    # course_title = serializers.SerializerMethodField()
    name = serializers.CharField(source='section')

    class Meta:
        model = CourseSubtitle
        fields = ['content','name','course_name','course_title','code']

    # def get_course_name(self, obj):
    #     return obj.course_name.name  # assuming 'name' is a field in Course model

    # def get_course_title(self, obj):
    #     return obj.course_title.chapter  # assuming 'title' is a field in CourseTitle model




class CourseTitleSerializer(serializers.ModelSerializer):
    section = CourseSubtitleSerializer(many=True, read_only=True)
    class Meta:
        model = CourseTitle
        fields = ['id', 'chapter', 'section']


class CourseSerializer(serializers.ModelSerializer):
    titles = CourseTitleSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'name', 'is_pro','description' , 'image', 'video', 'titles']



class CourseNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'is_pro','image']


class CourseNameSerializerById(serializers.ModelSerializer):
    titles = CourseTitleSerializer(many=True,read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'name', 'is_pro','image','titles']





class CourseChapterSerializer(serializers.ModelSerializer):
    course_title = serializers.PrimaryKeyRelatedField(queryset=CourseTitle.objects.all())

    class Meta:
        model = CourseSubtitle
        fields = ['id', 'section', 'content', 'course_title']


class CourseSubtitleCreateSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=True)
    course_title = serializers.PrimaryKeyRelatedField(queryset=CourseTitle.objects.all(), required=True)

    class Meta:
        model = CourseSubtitle
        fields = ['course', 'course_title', 'section', 'content']

    def validate(self, data):
        course = data.get('course')
        course_title = data.get('course_title')

        # بررسی اینکه course_title به course مربوط است یا خیر
        if course_title.course != course:
            raise serializers.ValidationError("عنوان انتخاب شده به دوره انتخاب شده تعلق ندارد.")
        return data
    


