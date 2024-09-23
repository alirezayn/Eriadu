from django.urls import path

from .views import *

urlpatterns = [
    path('execute/',execute_code,name="code"),
    path('execute_js/',execute_js,name="code"),
    path('execute_safe/',execute_safe,name="code"),
    path('chat_gpt/',chat_gpt,name="code"),

]