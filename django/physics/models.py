from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    title = models.TextField()
    slug = models.SlugField(default='', unique=True)
    pub_date = models.DateTimeField("Date published", default = timezone.now)
    difficulty = models.IntegerField(default=1)
    content = models.TextField(default = "No content yet")

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        kwargs = {
            # 'pk': self.id,
            'slug': self.slug
        }
        return reverse('post_detail', kwargs=kwargs)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)




class PostTopic(models.Model):
    Post = models.ForeignKey(Post, related_name='topics', on_delete=models.CASCADE)
    topic = models.TextField()

    def __str__(self):
        return self.topic

class PostViews(models.Model):
    Post = models.ForeignKey(Post, related_name='views', on_delete=models.CASCADE)
    call_date = models.DateTimeField("View-date", default = timezone.now)

    def __str__(self):
        return self.post