from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import NotificationSerializer
from firebase_admin import messaging
from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *
# تابع برای ارسال نوتیفیکیشن با استفاده از Firebase
def send_notification_to_user(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )

    try:
        response = messaging.send(message)
        return response
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

# View API برای ارسال نوتیفیکیشن
class SendNotificationView(APIView):
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            title = serializer.validated_data['title']
            body = serializer.validated_data['body']

            # فراخوانی تابع ارسال نوتیفیکیشن
            result = send_notification_to_user(token, title, body)

            if result:
                return Response({"message": "Notification sent successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to send notification"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaveTokenView(APIView):
    def post(self, request: Request):
        user = request.user
        token = request.query_params.get('token')

        # پیدا کردن یا ایجاد کردن توکن برای کاربر
        user_token, created = UserToken.objects.get_or_create(
            user=user,
            defaults={'token': token}  # اگر وجود نداشت، این توکن ثبت شود
        )

        if not created:
            # اگر توکن از قبل وجود داشت، آن را آپدیت کن
            user_token.token = token
            user_token.save()

        return Response({
            "success": True,
            "created": created  # برای نشان دادن آیا رکورد جدید ایجاد شد یا نه
        }, status=status.HTTP_201_CREATED)
    


# http://192.168.88.67:8000/notification/save-token/