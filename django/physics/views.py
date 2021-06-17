from django.shortcuts import render
from django.http import HttpResponse
# from django.template import loader
from .models import Post
from django.db.models import F

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
            "id" : p.id,
            "title" : p.title,
            "content" : md.convert(content_short),
            "topics": p.topics.all(),
            "date" : p.pub_date,
        }
        overview.append(data)
    context = {"post_list" : overview}
    return render(request, "physics/overview.html", context)


def expand_post(request, post_id):
    p = Post.objects.get(id=post_id)
    p.views += 1
    p.save()
    print(type(p.pub_date))
    context = {
        "title" : p.title,
        "content" : md.convert(p.content),
        "date" : p.pub_date.date(),
        "topics": p.topics.all(),
        "views": p.views,
        "toplinks" : get_toplinks(int(post_id)),
        }
    return render(request, "physics/post.html", context)
# Create your views here.

def get_toplinks(post_id):
    links = [
        {"text":'<i class="fa fa-angle-left"></i> Previous post', "url": "/physics/{}".format(post_id - 1)},
        {"text":'Next post <i class="fa fa-angle-right"></i>', "url": "/physics/{}".format(post_id + 1)}
    ]
    if post_id == 1:
        links.pop(0)
    elif post_id == Post.objects.count():
        links.pop(1)

    return links
