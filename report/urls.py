from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
route = DefaultRouter()


urlpatterns = [

    path('factor/',view=FactorReportView.as_view(),name='factor_report'),
    path('factor/<int:id>/', FactorDetailView.as_view(), name='factor-detail'),
    path('rate/',view=ReportRateView.as_view(),name="rate"),
    path('user/',view=UserReportView.as_view(),name="user"),
    path('user_report/',view=UserReportByIdReport.as_view(),name='user_api_report'),
    path('user_id_report/',view=UserReportByIdReportForAdmin.as_view(),name='user_api_report_allowe')

]