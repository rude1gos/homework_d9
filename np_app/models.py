from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)


    def update_rating(self):
        rating_of_posts_by_author = Post.objects.filter(author=self).aggregate(Sum('rate_post'))['rate_post__sum'] * 3
        rating_of_comments_by_author = Comment.objects.filter(user=self.user).aggregate(Sum('rate'))['rate__sum']
        rating_of_comments_under_posts_of_author = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rate'))['rate__sum']
        self.rate = rating_of_posts_by_author + rating_of_comments_by_author + rating_of_comments_under_posts_of_author
        self.save()

    def __str__(self):
        return f'{self.user}, рейтинг: {self.rate}'


class Category(models.Model):
    genre = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='SubscribersUser')

    def __str__(self):
        return f'{self.genre}'


class Post(models.Model):
    article = 'Arti'
    news = 'News'
    POSTS = [
        (article, 'Статья'),
        (news, 'Новости')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice = models.CharField(max_length=4, choices=POSTS, default=article)
    time_create_post = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header_post = models.CharField(max_length=255)
    text_post = models.TextField()
    rate_post = models.IntegerField(default=0)

    def preview(self):
        return f'{self.text_post[0:124]}...'

    def like(self):
        self.rate_post += 1
        self.save()

    def dislike(self):
        self.rate_post -= 1
        self.save()

    def __str__(self):
        return f'{self.author} - {self.header_post.title()}: {self.text_post}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class SubscribersUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField(null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()


class Appointment(models.Model):
    date = models.DateField(default=datetime.utcnow)
    user_name = models.CharField(max_length=200, null=True)
    message = models.TextField()

    def __str__(self):
        return f'{self.user_name}: {self.message}'