from rest_framework import serializers
from .models import Course, CourseExam, CourseTitle,CourseSubtitle,QuestionTitleSection, SubSection, SubSectionContent,CourseIntroduction, TitleInteraction

class AddCourseTitleSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(slug_field='name', queryset=Course.objects.all())
    chapter = serializers.CharField()
    class Meta:
        model = CourseTitle
        fields = ['id','course', 'chapter']



class QuestionTitleSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTitleSection
        fields = ['id', 'title', 'option_1', 'option_2', 'option_3', 'option_4', 'answer']
        # fields = '__all__'



class SubSectionContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSectionContent
        fields = '__all__'
        # fields = ['id','content','priority','code']


class SubSectionSerializer(serializers.ModelSerializer):
    sub_section_content = SubSectionContentSerializer(many=True,read_only=True)
    class Meta:
        model = SubSection
        fields = ['id','title','image','sub_section','sub_section_content']
        # fields = '__all__'

class CourseSubtitleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='section')
    sub_section = SubSectionSerializer(many=True,read_only=True)
    class Meta:
        model = CourseSubtitle
        fields = ['id','content','name','course_name','course_title','code','sub_section']
        # fields = '__all__'

    # def get_course_name(self, obj):
    #     return obj.course_name.name  # assuming 'name' is a field in Course model

    # def get_course_title(self, obj):
    #     return obj.course_title.chapter  # assuming 'title' is a field in CourseTitle model





class CourseTitleSectionSerializer(serializers.ModelSerializer):
    section = CourseSubtitleSerializer(many=True,read_only =True)
    class Meta:
        model = CourseTitle
        fields = ['id','section']




class TitleInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleInteraction
        fields = ["watched","locked"]


class CourseTitleSerializer(serializers.ModelSerializer):
    section = CourseSubtitleSerializer(many=True, read_only=True)
    question = QuestionTitleSectionSerializer(many=True, read_only=True) 
    watched = serializers.SerializerMethodField()
    locked = serializers.SerializerMethodField()

    # Class-level variable to track first title
    is_first_title = True

    class Meta:
        model = CourseTitle
        fields = ['id', 'chapter', 'question', 'watched', 'locked', 'section',]

    def get_watched(self, obj):
        user = self.context['request'].user
        interaction = TitleInteraction.objects.filter(title=obj, user=user).first()
        return interaction.watched if interaction else False

    def get_locked(self, obj):
        user = self.context['request'].user
        interaction = TitleInteraction.objects.filter(title=obj, user=user).first()

        if self.is_first_title:
            self.is_first_title = False  # Mark as processed for the first title
            return False  # Return False for the first title
        else:
            return interaction.locked if interaction else True  # For other titles, use the default logic
    


class CourseIntroSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseIntroduction
        fields = '__all__'



class CourseIntroductionSerializer(serializers.ModelSerializer):
    course_intro = CourseIntroSerializer(many=True)
    class Meta:
        model = Course
        fields = ['id', 'name','image','is_pro','course_intro']





class CourseSerializer(serializers.ModelSerializer):
    titles = CourseTitleSerializer(many=True, read_only=True)
    # course_intro = CourseIntroSerializer(many=True)
    class Meta:
        model = Course
        fields = ['id', 'name','is_pro','description', 'image', 'video', 'titles']






class CourseNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'is_pro', 'image']


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
    


class QuestioSectionSerialzer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=CourseTitle.objects.all())
    class Meta:
        model = QuestionTitleSection
        fields = '__all__'




class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseExam
        fields = '__all__'

        
class CourseExamSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(many=True)
    class Meta:
        model = Course
        fields = ['id','name','exam']


class CourseTitleQuestionSerializer(serializers.ModelSerializer):
    question = QuestionTitleSectionSerializer(many=True, read_only=True) 
    class Meta:
        model = CourseTitle
        fields = ['question']


