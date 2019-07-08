"""rest_admin6 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers
from users.views import UserViewset, AdminViewset,SmsForNewViewset, SmsForExistedViewset, UserMobileResetPasswordViewset
router = routers.DefaultRouter()
# 配置users的url
router.register(r'users', UserViewset, base_name='users')
# 配置新用户注册，更换注册手机的url
router.register(r'code/new', SmsForNewViewset, base_name='code/new')
# 配置老用户修改密码的url
router.register(r'code/existed', SmsForExistedViewset, base_name='code/existed')
# 配置admin的url
router.register(r'admin', AdminViewset, base_name="admin")
#配置短信接收修改密码
router.register(r'mobileresetpassword', UserMobileResetPasswordViewset, base_name='mobileresetpassword')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    # 调试登录
    path('api-auth/', include('rest_framework.urls')),
    # jwt的token认证
    path('jwt_login/', obtain_jwt_token),
    # path('code', include('users.urls', namespace='code'))
]

