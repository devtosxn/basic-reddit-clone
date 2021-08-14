from django.urls import path, include

from .views import PostView, PostDetailView


urlpatterns = [
    path('posts/', PostView.as_view(), name='posts'),
    path('posts/<uuid:id>/', PostDetailView.as_view(), name='post-detail'),
]
