from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Post_djb:
    class Status(models.TextChoices):
        DRAFT = 'd', 'Draft'
        PUBLISHED = 'p', 'Published'
        
    title = models.CharField(max_length=87)
    slug = models.SlugField(max_length=87)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.DRAFT)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    