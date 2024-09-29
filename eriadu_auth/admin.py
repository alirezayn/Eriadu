from django.contrib import admin
from .models import CustomUser,LimitedAccess
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(LimitedAccess)