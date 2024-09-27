from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Factor)
admin.site.register(CoursePlan)
# admin.site.register(Payment)
# admin.site.register(PaymentStats)