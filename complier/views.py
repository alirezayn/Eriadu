from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import subprocess
import tempfile
from openai import OpenAI
from django.http import HttpRequest
client = OpenAI(
  api_key="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",
  organization='org-Qi1wKCtqityprA3uQiAO1Arh',
)
@api_view(['POST'])
def execute_code(request):
    data = request.data
    code = data.get('code')

    if not code:
        return JsonResponse({'error': 'No code provided'}, status=400)

    try:
        result = subprocess.run(['python3', '-c', code], capture_output=True, text=True)
        return JsonResponse({'stdout': result.stdout, 'stderr': result.stderr})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@api_view(['POST'])
def execute_js(request):
    data = request.data
    code = data.get('code')

    if not code:
        return JsonResponse({'error': 'No code provided'}, status=400)

    try:
        result = subprocess.run(['node', '-e', code], capture_output=True, text=True)
        return JsonResponse({'stdout': result.stdout, 'stderr': result.stderr})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



@api_view(['POST'])
def execute_safe(request):
    data = request.data
    code = data.get('code')
    user_input = data.get('input', '')  # ورودی کاربر

    if not code:
        return JsonResponse({'error': 'No code provided'}, status=400)

    try:
        # ایجاد یک فایل موقت برای ذخیره کد
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
            temp_file.write(code.encode('utf-8'))
            temp_file_path = temp_file.name

        # اجرای کد در یک subprocess
        result = subprocess.run(['python', temp_file_path], input=user_input, capture_output=True, text=True)

        # حذف فایل موقت
        os.remove(temp_file_path)

        # بررسی وجود خطا در خروجی
        if result.returncode != 0:
            return JsonResponse({'error': result.stderr}, status=400)

        return JsonResponse({'stdout': result.stdout}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    




@api_view(['POST'])
def chat_gpt(request):
    data = request.data
    code = data.get('code')
    if not code:
        return JsonResponse({'error': 'No code provided'}, status=400)

    try:
        # تابعی برای جمع‌آوری پاسخ
        def gpt_stream():
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",  # یا مدل مورد نظر خود
                messages=[{"role": "user", "content": f"{code}\nخروجی کد رو با پایتون بده"}],  # پیام ورودی
                stream=True
            )
            response_content = ''
            for chunk in stream:
                if 'content' in chunk['choices'][0]['delta']:
                    # اضافه کردن تکه‌های استریم شده به پاسخ
                    response_content += chunk['choices'][0]['delta']['content']
            return response_content

        # جمع‌آوری پاسخ
        answer = gpt_stream()

        return JsonResponse({
            "answer": answer,
            "success": True,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



def render_http(request:HttpRequest):
    if request.method  == "POST":
        data = request.POST.get("page")
        return render(data)