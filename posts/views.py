from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import  Response
from .serializer import PostSerializer,LikeSerializer,LikepostSerializer
from .models import Post,Like
from .utils import Util
import sys
sys.path.append(".")
from api.models import User
from django.db.models import Q
from rest_framework import permissions
from .permissions import IsOwner
from django.conf import settings
import jwt

class PostListAPIView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        queryset = Post.objects.all()
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        token = request.headers['Authorization'].split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        user = User.objects.get(id=payload['user_id'])
        _dict ={
            'user_id': user.id,
            'username':user.username,
            'post_content': request.data['post_content'],
            'likes': 0
        }
        serializer = self.serializer_class(data=_dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PostuserAPIView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        token = request.headers['Authorization'].split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        user = User.objects.get(id=payload['user_id'])
        queryset = Post.objects.filter(username = user.username)
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LikeAPIView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        querset= Like.objects.all()
        serializer = self.serializer_class(querset,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        #import pdb;pdb.set_trace()
        token = request.headers['Authorization'].split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        user = User.objects.get(id=payload['user_id'])
        post = Post.objects.get(id=request.data['post_id'])
        _dict = {
            'post_id': post.id,
            'action_user_id': user.id,
            'type': request.data['type']
        }
        serializer = self.serializer_class(data=_dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        post_owner = User.objects.get(id=post.user_id.id)
        if request.data['type'] == 1:
            post.likes = post.likes + 1
        else:
            post.likes = post.likes - 1
        post.save()

        email_body = 'Hi ' + post_owner.username + \
                     'your post have been liked by ' + user.username
        # change email to post_owner.email
        data = {'email_body': email_body, 'to_email': 'tejazap@gmail.com',
                'email_subject': 'post liked'}

        Util.send_email(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LikePostAPIView(generics.GenericAPIView):
    serializer_class = LikepostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, post_id, action_user_id=None):
        token = request.headers['Authorization'].split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        user = User.objects.get(id=payload['user_id'])
        if Like.objects.filter(Q(post_id=post_id) & Q(action_user_id = user.id)):
            if Like.objects.filter(Q(post_id = post_id) & Q(action_user_id = user.id)).latest('created_on').type ==1:
                return Response({"user_like":"True"}, status=status.HTTP_200_OK)
        return Response({"user_like": "False"}, status=status.HTTP_200_OK)
