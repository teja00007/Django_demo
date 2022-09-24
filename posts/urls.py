from django.urls import path
from .views import PostListAPIView,PostuserAPIView,LikeAPIView

urlpatterns = [
    path('posts/', PostListAPIView.as_view(),name='post'),
    path('userposts/', PostuserAPIView.as_view(), name="postupdate"),
    path('Like/', LikeAPIView.as_view(), name="Like"),
]
