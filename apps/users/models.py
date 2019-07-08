from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.
class UserProfile(AbstractUser):
    """用户表"""
    username = models.CharField(max_length=50, default="", blank=True, verbose_name="用户名", help_text="用户名")
    gender_choice = (("male","男"),("female","女"))
    gender = models.CharField(choices=gender_choice, max_length=6, default="male", verbose_name="性别", help_text="性别")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月", help_text="出生年月")
    mobile = models.CharField(max_length=11, default="", blank=True, verbose_name="电话", help_text="电话")
    email = models.CharField(max_length=100, default="", blank=True, verbose_name="邮箱", help_text="邮箱")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class VerifyCode(models.Model):
    """
    短信验证码,回填验证码进行验证
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class EmailVerifyRecord(models.Model):
    send_choices = (("register","注册"),("forget","找回密码"),("update_email", "修改邮箱"))
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(choices=send_choices, max_length=20, verbose_name="验证码类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    # 重载str方法使后台不再直接显示object
    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)