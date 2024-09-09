# myapp/views.py
from rest_framework.response import Response

from rest_framework import generics, permissions,viewsets,status
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer
from .models import CustomUser
from .permission import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
user = get_user_model()

class CreateUserView(generics.CreateAPIView):
    model = user
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CustomUserSerializer


class ShowUserViewSet(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = [IsAdminUser]



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     try:
    #         serializer.is_valid(raise_exception=True)
    #     except Exception as e:
    #         return Response({"detail": "نام کاربری یا کلمه عبور اشتباه است"}, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(serializer.validated_data, status=status.HTTP_200_OK)