from django.contrib import admin
from .models import Post, PostTopic

# from django.admin import InlineModelAdmin


# Register your models here.
class TopicInlineFormset(admin.StackedInline):
    model = PostTopic
    extra = 0


class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = [TopicInlineFormset]

admin.site.register(Post, PostAdmin)
