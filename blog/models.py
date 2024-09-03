from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post_djb.Status.PUBLISHED)

class Post_djb(models.Model):
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
    
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    
    def __str__(self):
        return self.title  
        
    def get_absolute_url(self):
        """
        Returns the absolute URL of this Post_djb instance.

        :return: The absolute URL of this Post_djb instance.
        """
        return reverse("blog:post_detail", args=[self.id])



