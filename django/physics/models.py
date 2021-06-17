from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.TextField()
    pub_date = models.DateTimeField("Date published",default = timezone.now)
    difficulty = models.IntegerField(default=1)
    content = models.TextField(default = "No content yet")

    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class PostTopic(models.Model):
    Post = models.ForeignKey(Post,  related_name='topics', on_delete=models.CASCADE)
    topic = models.TextField()

    def __str__(self):
        return self.topic