from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post_djb.Status.PUBLISHED)

class Post_djb(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'd', 'Draft'
        PUBLISHED = 'p', 'Published'
        
    title = models.CharField(max_length=87)
    slug = models.SlugField(max_length=87, unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.DRAFT)
    
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    
    def __str__(self):
        """
        Returns a string representation of this post, which is
        simply its title.
        """ 
        return self.title  
        
    def get_absolute_url(self):
        """
        Returns the absolute URL of this post, using the post's
        publish date and slug as the URL parameters.
        """
        return reverse("blog:post_detail", args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
            ])


class Comment_djb(models.Model):
    post = models.ForeignKey(
        Post_djb,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

 