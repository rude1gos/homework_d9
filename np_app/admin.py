from django.contrib import admin
from .models import Post, Author, PostCategory

admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Author)