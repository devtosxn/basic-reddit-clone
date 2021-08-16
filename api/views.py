from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status, permissions, exceptions

from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer

from helpers.response import Response


class PostView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response({'posts': serializer.data, 'total': queryset.count()}, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Post.objects.all()
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def get(self, request, id):
        try:
            post = Post.objects.get(id=id)
            serializer = PostSerializer(post)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(errors={'detail': 'post does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = PostSerializer(
            instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'data': {}}, status=status.HTTP_204_NO_CONTENT)


class VoteView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        voter = self.request.user
        post = Post.objects.get(id=self.kwargs['id'])
        return Vote.objects.filter(voter=voter, post=post)

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs['id'])
        serializer.save(voter=self.request.user, post=post)

    def create(self, request, *args, **kwargs):
        serializer = VoteSerializer(data=request.data)
        if self.get_queryset().exists():
            return Response(errors={'detail': 'you have already voted for this post'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
