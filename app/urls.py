from django.urls import path
from .views import RetrievePost, UserRegistration, UserLoginView,CreatePostView,GetAllPOst,UpdateAPIView
urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('posts-list/',GetAllPOst.as_view(),name="posts-list"),
    path('posts/',CreatePostView.as_view(),name="posts"),
    path('posts/<int:pk>/',RetrievePost.as_view(),name="posts"),
    path('posts-update-destroy/<int:pk>/',UpdateAPIView.as_view(),name="posts-update-destroy")

]
