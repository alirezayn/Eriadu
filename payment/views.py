import traceback
from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse,HttpResponseRedirect,Http404
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token
import uuid
from eriadu_auth.models import CustomUser,LimitedAccess
from django.views.decorators.csrf import csrf_exempt
from course.models import Course
from datetime import datetime
from .models import Factor,CoursePlan
import requests
from dateutil.relativedelta import relativedelta
import json
from rest_framework.decorators import api_view
url_payping = 'https://api.payping.ir/v2/pay' 
@api_view(['GET'])
def get_csrf_token(request):
    """
    این ویو یک CSRF token جدید تولید کرده و به کاربر بازمی‌گرداند.
    """
    csrf_token = get_token(request)  # تولید CSRF Token
    return JsonResponse({'csrfToken': csrf_token})
# d0pda||waAZg21Wo

def payment(request: HttpRequest):
    if request.method == 'GET':
        data = {
            "phone": request.GET.get('phone'),
            "desc": request.GET.get('desc'),
            "amount": request.GET.get('amount'),
            "name": request.GET.get('name'),
        }

        phone = request.GET.get('phone')
        course = request.GET.get('course')
        plan = request.GET.get('plan')
        user = CustomUser.objects.get(user_phone = phone)
        course_id = Course.objects.get(id=course)
        plan_id = CoursePlan.objects.get(id=plan)
        if user and course_id and plan_id:
            Factor.objects.create(
                user = user,
                course=course_id,
                payed=False,
                plan=plan_id,
            )
            return render(request=request, template_name='shop.html', context=data)
        else:
            return HttpResponse("user or course or plan didnt retrun")

    if request.method == "POST":
        print(request.POST)
        client_ref_id = uuid.uuid4()
        data = {
            "amount": request.POST.get('amount'),
            "payerIdentity": request.POST.get('phone'),
            "payerName": request.POST.get('name'),
            "description": request.POST.get('desc'),
            "returnUrl": "http://192.168.11.2:8000/payment/factor_payed/",
            "clientRefId": str(client_ref_id)
            }
        Factor.objects.create(
                amount = data['amount'],
                payer_identity = data['payerIdentity'],
                payer_name = data['payerName'],
                description = data['description'],
                clientrefid = data['clientRefId']
                )
        headers = {
            "Authorization": "Bearer uCb_w5gEIm5ZBVeZgVYkaeCJtDOy49XY1mM_ls3-Wqs",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        resonse = requests.post(url_payping,json=data,headers=headers)
        print(resonse.text)
        if resonse.status_code == 200:
            code = resonse.json()
            return HttpResponseRedirect(f"https://api.payping.ir/v2/pay/gotoipg/{code['code']}") 



def testPaymeny(request:HttpRequest):
    if request.method == "POST":
        response_body = json.loads(request.body)
        clientrefid = uuid.uuid4()
        buyer = CustomUser.objects.get(id=response_body['user_id'])
        plan_id = CoursePlan.objects.get(id=response_body['plan_id'])
        # course = Course.objects.get(id=response_body['course'])
        Factor.objects.create(
            user= buyer,
            plan = plan_id,
            amount = response_body['amount'],
            payer_identity = response_body['payer_identity'],
            payer_name = response_body['payer_name'],
            clientrefid = clientrefid
        )
        return JsonResponse({
            'clientrefid':str(clientrefid)
        })
    return HttpResponse("hello")



def factor_view(request:HttpRequest):

    if request.method == "GET":
        query = request.GET.get('clientrefid')
        factor = Factor.objects.get(clientrefid=query)
        return render(request=request,template_name='shop.html',context={"factor":factor})

    if request.method == "POST":
        query = request.GET.get('clientrefid')
        factor = Factor.objects.get(clientrefid=query)
        data = {
            "amount": factor.amount,
            "payerIdentity": factor.payer_identity,
            "payerName": factor.payer_name,
            "description": "پرداخت برای خرید دوره",
            "returnUrl": "https://alirezayn.pythonanywhere.com/payment/factor_payed/",
            "clientRefId": str(factor.clientrefid)
            }
        headers = {
                "Authorization": "Bearer uCb_w5gEIm5ZBVeZgVYkaeCJtDOy49XY1mM_ls3-Wqs",
                "Accept": "application/json",
                "Content-Type": "application/json"
                }
        resonse = requests.post(url_payping,json=data,headers=headers)
        print(resonse.text)
        if resonse.status_code == 200:
            code = resonse.json()
            return HttpResponseRedirect(f"https://api.payping.ir/v2/pay/gotoipg/{code['code']}") 




@csrf_exempt
@require_POST
def payment_callback(request: HttpRequest):

    if request.method == 'POST':
        print("POST data received:", request.POST)

        code = request.POST.get('code')
        refid = request.POST.get('refid')
        clientrefid = request.POST.get('clientrefid')
        cardnumber = request.POST.get('cardnumber')
        cardhashpan = request.POST.get('cardhashpan')
        if cardnumber:
            factor = Factor.objects.get(clientrefid=clientrefid)
            factor.payed = True
            factor.refid = refid
            factor.payment_code = code
            factor.save()

            user = CustomUser.objects.get(user_phone=factor.user.user_phone)
            
            if factor.plan.unlimited:
                user.is_pro = True
                user.unlimited =True
                user.save()
            elif factor.plan.year > 0:
                today = datetime.today()
                yearly_access = today + relativedelta(years=1)
                new = LimitedAccess.objects.create(
                    end_date = yearly_access
                )
                user.limited = new
                user.save()
            elif factor.plan.month > 0:
                today = datetime.today()
                monthly_access = today + relativedelta(month=factor.plan.month)
                new = LimitedAccess.objects.create(
                    end_date = monthly_access
                )
                user.limited = new
                user.save()

            data = {
                "refId": refid,
                "amount": factor.amount
            }
            headers = {
                "Authorization": "Bearer uCb_w5gEIm5ZBVeZgVYkaeCJtDOy49XY1mM_ls3-Wqs",
                "Accept": "application/json",
                "Content-Type": "application/json"
                }
            response = requests.post('https://api.payping.ir/v2/pay/verify',json=data,headers=headers)
            if response.status_code == 200:
                return HttpResponse("Payment successful")
        print(code,cardnumber)
        return HttpResponse("Payment Failed")
         