from django.db import models
from django.conf import settings
# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()

class UserToken(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,name='user_token',null=True,blank=True)
    firbase_token = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user} - {self.token[:10]}..."


