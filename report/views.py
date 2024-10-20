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
from jdatetime import date as jdate
from datetime import timedelta



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
    
    def get(self, request: Request):
        now = timezone.now()
        
        # گرفتن تاریخ شمسی جاری
        jalali_now = jdate.fromgregorian(date=now.date())
        start_of_jalali_month = jdate(jalali_now.year, jalali_now.month, 1)
        
        # تبدیل شروع و پایان ماه شمسی به میلادی
        start_of_month = start_of_jalali_month.togregorian()
        end_of_month = (start_of_jalali_month.replace(day=1) + timedelta(days=32)).replace(day=1).togregorian() - timedelta(seconds=1)

        # فیلتر کردن فاکتورهای ماه شمسی
        factors = Factor.objects.filter(
            created__gte=start_of_month,
            created__lte=end_of_month,
            payed=True
        )

        users = CustomUser.objects.filter(
            created__gte=start_of_month,
            created__lte=end_of_month,
        )

        # فیلتر روزانه
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        factors_daily = Factor.objects.filter(
            created__gte=start_of_day,
            created__lte=end_of_day,
            payed=True
        )

        users_daily = CustomUser.objects.filter(
            created__gte=start_of_day,
            created__lte=end_of_day,
        )

        # نام ماه جلالی
        month_name = jdate.j_months_fa[jalali_now.month - 1]

        return Response({
            "total_factors": factors.count(),
            "users": users.count(),
            "month": str(start_of_jalali_month),
            "month_name": month_name,
            "factor_daily": factors_daily.count(),
            "user_daily": users_daily.count(),
        })


class UserReportView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    

class UserReportByIdReport(ListAPIView):
   serializer_class = UserActivitySerializer
   def get_queryset(self):
       user = self.request.user
       return UserActivity.objects.filter(user=user)


class UserReportByIdReportForAdmin(ListAPIView):
    serializer_class = UserActivitySerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        
        user_id = self.request.query_params.get('id')
        print(user_id)
        user = CustomUser.objects.get(id=user_id)
        return UserActivity.objects.filter(user=user)