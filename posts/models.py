from django.db import models
from django.conf import settings

class Post(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    post_content = models.TextField()
    likes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    action_user_id = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    post_id = models.IntegerField()
    type = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)