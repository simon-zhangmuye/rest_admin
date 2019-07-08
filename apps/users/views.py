from django.shortcuts import render
from .serializers import UserMobileRegSerializer, UserDetailSerializer, SmsForNewSerializer, SmsForExistedSerializer, AdminSerializer, UserMobileResetPasswordSerializer
from rest_framework import mixins, permissions, authentication, viewsets, status
from random import choice
from utils.miaodisms import MiaoDiSMS
from .models import VerifyCode
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
# Create your views here.


class CustomBackend(ModelBackend):
    """
    自定义用户验证规则
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因
            # 后期可以添加邮箱验证
            user = User.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsForNewViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    给未注册用户发送验证码，修改注册手机
    """
    serializer_class = SmsForNewSerializer

    def generate_code(self):
        """
        生成四位数字的验证码字符串
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        miao_di = MiaoDiSMS()
        code = self.generate_code()
        sms_status = miao_di.send_sms(code=code, mobile=mobile)

        if sms_status["respCode"] == "00000":
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "mobile": sms_status["respDesc"]
            }, status=status.HTTP_400_BAD_REQUEST)


class SmsForExistedViewset(SmsForNewViewset):
    """
    给已经注册的用户发送短信验证码修改密码
    """
    serializer_class = SmsForExistedSerializer


class UserViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = []
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = []

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        if self.action == "create":
            return UserMobileRegSerializer
        if self.action == "update":
            return UserDetailSerializer
        return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated, )
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)



    # 重写该方法，不管传什么id，都只返回当前用户
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class AdminViewset(viewsets.ModelViewSet):
    serializer_class = AdminSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = [permissions.IsAdminUser]


class UserMobileResetPasswordViewset(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserMobileResetPasswordSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = []

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance =self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        user = self.perform_update(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.username

        headers = {}
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 重写该方法，不管传什么id，都只返回当前用户
    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        return serializer.save()

