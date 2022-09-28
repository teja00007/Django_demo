from rest_framework import serializers
from .models import Post,Like

class PostSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=False)
    likes = serializers.IntegerField(required=False)

    class Meta:
        model = Post
        fields = "__all__"

class LikeSerializer(serializers.ModelSerializer):

    post_id = serializers.IntegerField(required=True,write_only=False)
    type = serializers.IntegerField(write_only=True)

    class Meta:
        model = Like
        fields = "__all__"

class LikepostSerializer(serializers.ModelSerializer):

    post_id = serializers.IntegerField(required=True,write_only=False)
    type = serializers.IntegerField(write_only=True)
    action_user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Like
        fields = "__all__"