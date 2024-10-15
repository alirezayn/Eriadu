from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import *
from payment.models import *
from course.models import *
from eriadu_auth.models import *
from .serializers import *
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from jdatetime import date 



class FactorReportView(ListAPIView):
    queryset = Factor.objects.all()
    serializer_class = FactorReportSerializer
    permission_classes = [IsAdminUser]



class FactorRep():
    pass



class FactorDetailView(RetrieveAPIView):
    queryset = Factor.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = FactorReportDetailSerilizer
    lookup_field = 'id'



class ReportRateView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request:Request):

        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

        # فیلتر کردن فاکتورهایی که در ماه فعلی هستند و پرداخت شده‌اند
        factors = Factor.objects.filter(
            created__gte=start_of_month,
            created__lte=end_of_month,
            payed=True  # فرض بر اینکه فیلد 'payed' وضعیت پرداخت را مشخص می‌کند
        )

        # سریالایز کردن داده‌های فاکتور (در صورت نیاز به نمایش)
        factor_data = [factor.id for factor in factors]  # می‌توانید از سریالایزر هم استفاده کنید

        users = CustomUser.objects.filter(
            created__gte=start_of_month,
            created__lte=end_of_month,
        )
        # users_data = [user.id for user in users]
        jalali_date = date.fromgregorian(date=start_of_month)
        month_name = date.j_months_fa[jalali_date.month]



        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        # فیلتر کردن فاکتورهایی که در روز جاری هستند و پرداخت شده‌اند
        factors_daily = Factor.objects.filter(
            created__gte=start_of_day,
            created__lte=end_of_day,
            payed=True
        )

        # فیلتر کردن کاربرانی که در روز جاری اضافه شده‌اند
        users_daily = CustomUser.objects.filter(
            created__gte=start_of_day,
            created__lte=end_of_day,
        )

        # تبدیل تاریخ به شمسی


        return Response({
            "total_factors": factors.count(),
            # "factors": factor_data,
            "users":users.count(),
            "month":str(jalali_date),
            "month_name":month_name,
            "factor_daily":factors_daily.count(),
            "user_daily":users_daily.count(),
        })
    

class UserReportView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
