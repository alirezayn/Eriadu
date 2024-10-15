from django.urls import path
from .views import *

urlpatterns = [
    path('', search_all_models, name='search_all_models'),
    path('public/', search_specific_models, name='search_all_models'),
    path('user/',view=UserSearchView.as_view(),name="user_search")
]