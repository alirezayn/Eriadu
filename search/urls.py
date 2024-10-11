from django.urls import path
from .views import search_all_models,search_specific_models

urlpatterns = [
    path('', search_all_models, name='search_all_models'),
    path('public/', search_specific_models, name='search_all_models'),
]