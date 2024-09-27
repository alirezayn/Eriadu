from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

route = DefaultRouter()
route.register('users',viewset=AccessibleCourseViewSet)
route.register('profile',viewset=ShowUserViewSet)
route.register('factor',viewset=AllUserFactorDetails)

urlpatterns = [
    path('',include(route.urls)),
    path('register/', CreateUserView.as_view(), name='register'),
    path('verify-otp/',VerifyOTPView.as_view(),name='verifyOtp'),
    path('course/',UserCourseListApiView.as_view(),name='user_course')
]
