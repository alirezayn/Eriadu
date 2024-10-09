from django.urls import path,include
from .views import *


urlpatterns = [
    path('get_csrf_token/',view=get_csrf_token,name='get_token'),
    path('factor/',view=factor_view,name='factor_page'),
    path('factor_payed/',view=payment_callback,name='factor_submitted'),
    path('test_payment/',view=testPaymeny,name='test'),
    path('plans',view=PlanListView.as_view(),name='plans')
]