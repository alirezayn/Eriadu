
from eriadu_auth.models import CustomUser

def addCourseToUser(user_phone):
    user = CustomUser.objects.get(user_phone=user_phone)
    print(user)




