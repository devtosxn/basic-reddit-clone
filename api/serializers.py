from rest_framework import serializers

from .models import Post, Vote


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'updated_at',
                  'author')
        extra_kwargs = {'author': {'read_only': True}}


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id',)
