from django.shortcuts import render

from django.utils import timezone
import datetime
# from django.template import loader
from .models import Post

import markdown
md = markdown.Markdown(extensions=["markdown_katex"])


OVERVIEW_CUT = 100
def index(request):
    post_list = Post.objects.order_by("pub_date")
    
    overview = []
    for p in post_list:
        content_short = " ".join(p.content.split(" ")[:OVERVIEW_CUT]) + " ..." # shortened to the 100 first words.
        # TODO: verify if not breaking math. replace titles by bold text
        data = {
            "url" : "post/{}".format(p.slug),
            "title" : p.title,
            "content" : md.convert(content_short),
            "topics": p.topics.all(),
            "date" : p.pub_date,
        }
        overview.append(data)
    context = {"post_list" : overview}
    return render(request, "physics/overview.html", context)


def expand_post(request, slug):
    p = Post.objects.get(slug=slug)
    # increase count number:
    p.views.create(call_date=datetime.datetime.now(tz = timezone.utc))
    context = {
        "title" : p.title,
        "content" : md.convert(p.content),
        "date" : p.pub_date.date(),
        "topics": p.topics.all(),
        "views": p.views.count(),
        "toplinks" : get_toplinks(p.id),
        }
    return render(request, "physics/post.html", context)
# Create your views here.


def get_toplinks(post_id):
    links = {}
    try:
        prev = Post.objects.get(id=post_id - 1)
        links["previous"] = "/physics/post/{}".format(prev.slug)
    except:
        pass
    try:
        next = Post.objects.get(id=post_id + 1)
        links["next"] = "/physics/post/{}".format(next.slug)
    except:
        pass

    return links

