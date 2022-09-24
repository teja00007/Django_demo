from rest_framework import serializers
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth

#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = User
    fields = ('username', 'password', 'password2',
         'email', 'fullname')
    extra_kwargs = {
      'first_name': {'required': True},
      'last_name': {'required': True}
    }
  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  def create(self, validated_data):
    user = User.objects.create(
      username=validated_data['username'],
      email=validated_data['email'],
      fullname=validated_data['fullname']
    )
    user.set_password(validated_data['password'])
    user.save()
    return Response(user,status=status.HTTP_201_CREATED)

class EmailVerificationSerializer(serializers.ModelSerializer):
  token = serializers.CharField(max_length=555)

  class Meta:
    model = User
    fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255, min_length=3)
  password = serializers.CharField(
    max_length=68, min_length=6, write_only=True)
  username = serializers.CharField(
    max_length=255, min_length=3, read_only=True)

  tokens = serializers.SerializerMethodField()

  def get_tokens(self, obj):
    user = User.objects.get(email=obj['email'])

    return {
      'refresh': user.tokens()['refresh'],
      'access': user.tokens()['access']
    }

  class Meta:
    model = User
    fields = ['email', 'password','username', 'tokens']

  def validate(self, attrs):
    email = attrs.get('email', '')
    password = attrs.get('password', '')

    user = auth.authenticate(email=email, password=password)

    if not user:
      raise AuthenticationFailed('Invalid credentials, try again')
    if not user.is_active:
      raise AuthenticationFailed('Account disabled, contact admin')
    if not user.is_verified:
      raise AuthenticationFailed('Email is not verified')

    return {
      'email': user.email,
      'username': user.username,
      'tokens': user.tokens
    }

    return super().validate(attrs)