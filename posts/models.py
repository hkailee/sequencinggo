from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='posts_created')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='created')
    image = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now,
                                   db_index=True)
    updated = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='posts_voted',
                                        blank=True)

    status = models.CharField(max_length=10, default='published')

    objects = models.Manager() # The default manager.
    published = PublishedManager() # The Dahl-specific manager.                
                        
    tags = TaggableManager()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('posts:detail', args=[self.id, self.slug])



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='comments_created')
    body = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='comments_liked',
                                        blank=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user, self.post)



