from django.urls import path,include
from .views import *


urlpatterns = [
    path('factor/',view=payment,name='factor_page'),
    path('factor_payed/',view=payment_callback,name='factor_submitted')
]