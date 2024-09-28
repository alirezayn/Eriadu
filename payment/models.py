from django.db import models
from django.conf import settings
from course.models import Course

import uuid


class CoursePlan(models.Model):
    month = models.IntegerField(default=0,blank=True)
    year = models.IntegerField(default=0,blank=True)
    price = models.IntegerField(default=0,blank=True)
    discount = models.IntegerField(default=0,blank=True)

    def __str__(self) -> str:
        if self.month == 0:
            return f"پلن {self.year} ساله"
        else:
            return f"پلن {self.month} ماهه"

class Factor(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    payed = models.BooleanField(default=False)
    plan = models.ForeignKey(CoursePlan, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(null=True,blank=True)
    payer_identity = models.CharField(max_length=255, help_text="ایمیل یا شماره موبایل پرداخت‌کننده")
    payer_name = models.CharField(max_length=255, help_text="نام پرداخت‌کننده", null=True, blank=True)
    payment_code = models.CharField(max_length=255,null=True,blank=True)
    refid = models.CharField(max_length=255,null=True,blank=True)
    clientrefid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, help_text="کد ارجاع پی‌پینگ")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user_phone} فاکتور"

    class Meta:
        ordering = ['-created']



# class Factor(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     payed = models.BooleanField(default=False)
#     plan = models.ForeignKey(CoursePlan,on_delete=models.CASCADE)


#     def __str__(self) -> str:
#         return f"{self.user.user_phone} فاکتور"
    





# class Payment(models.Model):
#     amount = models.PositiveIntegerField()
#     payer_identity = models.CharField(max_length=255, help_text="ایمیل یا شماره موبایل پرداخت‌کننده")
#     payer_name = models.CharField(max_length=255, help_text="نام پرداخت‌کننده", null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     clientrefid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, help_text="کد ارجاع پی‌پینگ")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self): 
#         return f"Payment {self.client_ref_id} - {self.amount}"

#     class Meta:
#         ordering = ['-created_at']
#         verbose_name = "پرداخت"
#         verbose_name_plural = "پرداخت‌ها"


# class PaymentStats(models.Model):
#     payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,related_name='payment',null=True)
#     is_payed = models.BooleanField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     code = models.CharField(max_length=255)
#     refid = models.CharField(max_length=255)
#     clientrefid = models.CharField(max_length=255)
#     cardnumber = models.CharField(max_length=255)
#     cardhashpan = models.CharField(max_length=255)





