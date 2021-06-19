from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
import time

from physics.models import Post as ppost
# from blog.models import Post as bpost

import plotly.graph_objects as go
from plotly.offline import plot
from plotly.graph_objs import Scatter


card_str = """
<div class="card-body">
    <h5 class="card-title">{title}</h5>
    {content}
</div>
"""


def index(request):
    card = """
        <img src="https://dummyimage.com/600x400/000/fff.jpg" class="card-img-top" alt="...">
        <div class="card-body">
          <h5 class="card-title">Card title</h5>
          <p class="card-text">This is a longer card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
        </div>
    """
    context = {"card_list": []}

    context["card_list"].append({
        "content": async_card(
            "Total views",
            "total_views",
            "fetch_total_views"
            ),
        "width" : 4})


    context["card_list"].append({
        "content": async_card(
            "Post view ratio",
            "relative_views",
            "fetch_relative_views"
            ),
        "width" : 4})
    # context["card_list"].append({"content": card_relative_views(), "width" : 4})
    return render(request, "analytics/overview.html", context)


def async_card(title, id, func):
    loader = """
    <script>
    $(document).ready(
        function(){{
            $("#{id}").load("{url}");
        }}
    );
    </script>
    <div id="{id}" class="text-center">
        <div class="spinner-grow" role="status" >
            <span class="sr-only">Loading...</span>
        </div>
    </div>
    """
    loaded = loader.format(id=id, url=func)
    load_card = card_str.format(title=title, content=loaded)
    return load_card



    
def fetch_total_views(request):
    time.sleep(5)
    x_data = [0,1,2,3]
    y_data = [x**2 for x in x_data]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines', name='test', opacity=0.8, marker_color='green'))
    fig = cleanse_fig(fig)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return HttpResponse(plot_div)




def fetch_relative_views(request):
    values = []
    labels = []
    for plist in [ppost]:
        for post in plist.objects.all():
            values.append(post.views)
            labels.append(post.title)

    fig = go.Figure()
    fig.add_trace(go.Pie(labels = labels, values=values, textinfo="label"))
    fig = cleanse_fig(fig)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return HttpResponse(plot_div)







def get_cumulated():
    total_posts = 0
    total_views = 0
    for plist in [ppost]:
        total_posts += plist.objects.count()
        views = plist.objects.all().aggregate(Sum("views"))
        total_views += views["views__sum"]
    print(total_posts, total_views)    
    return total_posts, total_views


######## helper:
def cleanse_fig(fig):
    fig.layout.update(
            xaxis = {
                'showgrid': False, # thin lines in the background
                'zeroline': False, # thick line at x=0
                'visible': False,  # numbers below
            }, # the same for yaxis
            yaxis = {
                'showgrid': False, # thin lines in the background
                'zeroline': False, # thick line at x=0
                'visible': False,  # numbers below
            }, # the same for yaxis

            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',

            )
    return fig