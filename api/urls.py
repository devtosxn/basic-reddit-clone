from django.urls import path

from .views import PostView, PostDetailView, VoteView


urlpatterns = [
    path('posts/', PostView.as_view(), name='posts'),
    path('posts/<uuid:id>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<uuid:id>/vote/', VoteView.as_view(), name='vote'),
]
