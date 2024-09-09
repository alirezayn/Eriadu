from django.urls import path,include
from .views import CreateUserView,ShowUserViewSet,CustomTokenObtainPairView
from rest_framework.routers import DefaultRouter

route = DefaultRouter()
route.register('users',viewset=ShowUserViewSet)

urlpatterns = [
    path('',include(route.urls)),
    # path('register/', CreateUserView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
