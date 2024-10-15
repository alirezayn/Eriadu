from django.apps import apps
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import *
from deep_translator import GoogleTranslator
from eriadu_auth.models import CustomUser
from course.models import Course,CourseTitle,CourseIntroduction,CourseSubtitle,CourseExam
from report.serializers import UserSearchSerializer
from rest_framework.permissions import IsAdminUser
@api_view(['GET'])
def search_all_models(request):
    query = request.GET.get('q', '')
    results = {}

    if query:
        try:
            # ترجمه کوئری از انگلیسی به فارسی
            translated_query = GoogleTranslator(source='en', target='fa').translate(query)

            # دریافت تمام مدل‌های ثبت‌شده در اپلیکیشن
            all_models = apps.get_models()
            for model in all_models:
                # بررسی فیلدهای متنی برای جستجو
                model_name = model.__name__

                fields = [field.name for field in model._meta.fields if field.get_internal_type() in ['CharField', 'TextField']]

                if fields:
                    q_objects = Q()
                    for field in fields:
                        q_objects |= Q(**{f"{field}__icontains": query})  # جستجوی با متن اصلی
                        q_objects |= Q(**{f"{field}__icontains": translated_query})  # جستجوی با متن ترجمه‌شده

                    # اجرای جستجو در هر مدل
                    model_results = model.objects.filter(q_objects)

                    # افزودن نتایج به دیکشنری به همراه ID و توصیف
                    if model_results.exists():
                        results[model_name] = [{'id': result.id, 'description': str(result),'image':result.image} for result in model_results]

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    return Response(results)


@api_view(['GET'])
def search_specific_models(request):
    query = request.GET.get('q', '')
    results = {}

    # لیست مدل‌های خاص برای جستجو
    models_to_search = [Course, CourseTitle, CourseIntroduction, CourseSubtitle, CourseExam]

    model_aliases = {
        'Course': 'درس',
        'CourseTitle': 'تیتر',
        'CourseIntroduction': 'معرفی',
        'CourseSubtitle': 'سکشن',
        'CourseExam': 'آزمون'
    }

    # آدرس هاست به صورت دستی
    host_url = "http://alirezayn.pythonanywhere.com"

    if query:
        try:
            # ترجمه کوئری از انگلیسی به فارسی
            translated_query = GoogleTranslator(source='en', target='fa').translate(query)

            for model in models_to_search:
                model_name = model.__name__
                alias = model_aliases.get(model_name, model_name)
                fields = [field.name for field in model._meta.fields if field.get_internal_type() in ['CharField', 'TextField']]

                if fields:
                    q_objects = Q()
                    for field in fields:
                        q_objects |= Q(**{f"{field}__icontains": query})  # جستجوی با متن اصلی
                        q_objects |= Q(**{f"{field}__icontains": translated_query})  # جستجوی با متن ترجمه‌شده

                    # اجرای جستجو در هر مدل
                    model_results = model.objects.filter(q_objects)

                    # افزودن نتایج به دیکشنری به همراه ID و توصیف
                    if model_results.exists():
                        results[alias] = [{
                            'id': result.id,
                            'description': str(result),
                            'is_pro':result.is_pro if hasattr(result,'image') and result.is_pro else False,
                            'image': host_url + result.image.url if hasattr(result, 'image') and result.image else None
                        } for result in model_results]

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    return Response(results)


class UserSearchView(ListAPIView):

    serializer_class = UserSearchSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        queryset = CustomUser.objects.all()
        phone_number = self.request.query_params.get('phone', None)
        if phone_number:
            # جستجو با استفاده از بخش ورودی شماره تلفن
            queryset = queryset.filter(user_phone__icontains=phone_number)
        return queryset