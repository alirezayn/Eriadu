from django.apps import apps
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view
from deep_translator import GoogleTranslator
from course.models import Course,CourseTitle,CourseIntroduction,CourseSubtitle,CourseExam
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
                        results[model_name] = [{'id': result.id, 'description': str(result)} for result in model_results]

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    return Response(results)


@api_view(['GET'])
def search_specific_models(request):
    query = request.GET.get('q', '')
    results = {}
    
    # لیست مدل‌های خاص برای جستجو
    models_to_search = [Course,CourseTitle,CourseIntroduction,CourseSubtitle,CourseExam]

    model_aliases = {
        'Course': 'درس',
        'CourseTitle': 'تیتر',
        'CourseIntroduction': 'معرفی',
        'CourseSubtitle': 'سکشن',
        'CourseExam': 'آزمون'
    }
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
                        results[alias] = [{'id': result.id, 'description': str(result)} for result in model_results]

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    return Response(results)
