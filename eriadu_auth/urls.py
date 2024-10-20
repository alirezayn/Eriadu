from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

route = DefaultRouter()
route.register('users',viewset=AccessibleCourseViewSet)
route.register('list',viewset=FullUserList)
route.register('factor',viewset=AllUserFactorDetails)


urlpatterns = [
    path('',include(route.urls)),
    path('register/', CreateUserView.as_view(), name='register'),
    path('verify-otp/',VerifyOTPView.as_view(),name='verifyOtp'),
    path('course/',UserCourseListCreateView.as_view(),name='course'),
    path('user_course/',RetrieveUserCourseAPI.as_view(),name='user_courses'),
    path('login/', LoginPairView.as_view(), name='token_obtain_pair')

]