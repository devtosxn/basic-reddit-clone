from rest_framework.views import APIView
from rest_framework import generics, status, response

from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer

from helpers.response import Response


class PostView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
