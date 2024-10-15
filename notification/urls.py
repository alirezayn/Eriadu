from django.urls import path
from .views import *

urlpatterns = [
    path('send-notification/', SendNotificationView.as_view(), name='send-notification'),
    path('save-token/', SaveTokenView.as_view(), name='save-token'),
]
