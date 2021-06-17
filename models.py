
from django.db import models
from django.db.models.fields.files import ImageField
from froala_editor.fields import FroalaField
from django.conf import settings
from django.utils import timezone
from django.urls import reverse



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')




class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True,)
    author = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name='blog_posts')
    content = FroalaField(blank=True)
    image   = ImageField(upload_to='images/', blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='draft')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blog_post', blank=True)
    
    
    class Meta:
        ordering = ('-publish',)

    def total_likes(self):
        return self.likes.count()
        
    def __str__(self):
        return self.title

    objects = models.Manager() 
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=(str(self.id)))





