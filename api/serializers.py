from rest_framework import serializers

from .models import Post, Vote


class PostSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'updated_at',
                  'author', 'votes')
        extra_kwargs = {'author': {'read_only': True}}

    def get_votes(self, obj):
        return Vote.objects.filter(post=obj).count()


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id',)
