from django.contrib import admin
from .models import Post, Vote

admin.site.regsister(Post)
admin.site.register(Vote)

