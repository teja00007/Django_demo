from rest_framework import serializers
from .models import Post,Like

class PostSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=False)
    likes = serializers.IntegerField(required=False)

    class Meta:
        model = Post
        fields = "__all__"

class LikeSerializer(serializers.ModelSerializer):

    post_id = serializers.IntegerField(required=True)

    class Meta:
        model = Like
        fields = "__all__"