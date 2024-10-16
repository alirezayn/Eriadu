# myapp/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.core.validators import RegexValidator
from rest_framework_simplejwt.tokens import RefreshToken
from course.models import Course
from jdatetime import GregorianToJalali




class CustomUserManager(BaseUserManager):
    def create_user(self, user_phone, password=None, **extra_fields):
        if not user_phone:
            raise ValueError('The phone number must be set')
        user = self.model(user_phone=user_phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # This makes the password unusable if not provided
        user.save(using=self._db)
        return user

    def create_superuser(self, user_phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(user_phone, password, **extra_fields)



    def update_user(self, user, password=None, **extra_fields):
        for key, value in extra_fields.items():
            setattr(user, key, value)

        if password:  # اگر رمز عبور تغییر کرده باشد
            user.set_password(password)  # هش کردن رمز عبور

        user.save(using=self._db)
        return user



class CustomUser(AbstractBaseUser, PermissionsMixin):


    phone_validator = RegexValidator(regex=r'^09\d{9}$', message="Phone number must be 11 digits.")
    username = models.CharField(unique=True,null=True,max_length=50)
    email = models.EmailField(unique=True,null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    user_phone = models.CharField(max_length=11,unique=True,validators=[phone_validator])
    is_active = models.BooleanField(default=False,verbose_name="کاربر فعال")
    is_staff = models.BooleanField(default=False)
    is_pro = models.BooleanField(default=False)
    courses = models.ManyToManyField(Course, related_name='allowed_users', blank=True)
    image_profile = models.ImageField(upload_to='static/users/profile/',blank=True)
    unlimited = models.BooleanField(default=False)
    limited = models.ForeignKey('LimitedAccess',on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)


    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Adding related_name to avoid conflicts
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Adding related_name to avoid conflicts
        blank=True
    )

    objects = CustomUserManager()


    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'user_phone'

    def __str__(self):
        return self.user_phone


    def get_token(self):
        refresh = RefreshToken.for_user(self)
        refresh['username'] = self.username  # می‌توانید فیلدهای دیگر مثل email یا role را هم اضافه کنید
        refresh['email'] = self.email
        refresh['first_name'] = self.first_name
        refresh['last_name'] = self.last_name
        refresh['is_active'] = self.is_active
        refresh['user_phone'] = self.user_phone
        return refresh



class OTP(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)



class LimitedAccess(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def get_start_date_jalali(self):
        start_date = GregorianToJalali(
            gyear=self.start_date.year,
            gmonth=self.start_date.month,
            gday=self.start_date.day
        )
        return f"{start_date.jyear}/{start_date.jmonth}/{start_date.jday}"


    def get_end_date_jalali(self):
        end_date = GregorianToJalali(
            gyear=self.end_date.year,
            gmonth=self.end_date.month,
            gday=self.end_date.day
        )
        return f"{end_date.jyear}/{end_date.jmonth}/{end_date.jday}"


    def __str__(self) -> str:
        start_jalali = self.get_start_date_jalali()
        end_jalali = self.get_end_date_jalali()
        return f"از تاریخ {start_jalali} تا {end_jalali}"




class UserCourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')



class UserActivity(models.Model):
    total = models.IntegerField(default=0)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    