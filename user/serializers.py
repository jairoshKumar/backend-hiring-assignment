from rest_framework import serializers
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=False)

#     class Meta:
#         model = User
#         fields = ('email', 'password', 'full_name',
#                   'mobile', 'user_type', 'user_subtype')

#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         user = User.objects.create(
#             **validated_data, username=validated_data.get("email"))
#         user.set_password(password)
#         user.save()
#         # Here, you can also generate and send the OTP for email verification
#         return user


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

#     class Meta:
#         fields = ["username", "password"]

#     @csrf_exempt
#     def validate(self, data):
#         username = data.get("username", "")
#         password = data.get("password", "")

#         if username and password:
#             probable_user = User.objects.filter(username=username).first()

#             if probable_user:
#                 if probable_user.has_usable_password():
#                     try:
#                         user = authenticate(
#                             username=username, password=password)
#                         if user:
#                             if user.is_active:
#                                 data["user"] = user
#                                 data["status"] = True
#                             else:
#                                 data["status"] = False
#                                 data["error_code"] = 403
#                         else:
#                             data["status"] = False
#                             data["error_code"] = 406
#                     except User.DoesNotExist as e:
#                         data["status"] = False
#                         data["error_code"] = 402
#                 else:
#                     data["status"] = False
#                     data["error_code"] = 405
#             else:
#                 data["status"] = False
#                 data["error_code"] = 404
#         else:
#             msg = "Must provide mobile and password both"
#             data["status"] = False
#             data["error_code"] = 401
#         return data

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'