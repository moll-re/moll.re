from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum, Count
from django.db.models.functions import Trunc

import time

from physics.models import Post as ppost
post_list = [ppost]
from .models import SensorMetric as sensor

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
            "Total views (hourly)",
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

    context["card_list"].append({
        "content": async_card(
            "Sensor metrics",
            "aio_sensors",
            "fetch_aio_sensors"
            ),
        "width" : 4})
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
    qs = []
    for plist in post_list:
        for post in plist.objects.all():
            vh = post.views\
                .annotate(hour=Trunc('call_date', 'hour'))\
                .values('hour')\
                .annotate(call=Count('id'))
            qs.append(vh)

    new_qs = qs[0].union(*qs[1:]) # merged but somehow not enough
    # TODO: make more efficient
    hours = []
    calls = []
    for q in list(new_qs):
        try:
            i = hours.index(q["hour"])
            calls[i] += q["call"]
        except: # element does not yet exist
            hours.append(q["hour"])
            calls.append(q["call"])

    fig = go.Figure()
    fig.layout.update(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis = dict(range=[hours[-24], hours[-1]])

    )
    fig.add_trace(go.Bar(x=hours, y=calls))
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return HttpResponse(plot_div)



def fetch_relative_views(request):
    values = []
    labels = []
    for plist in [ppost]:
        for post in plist.objects.all():
            values.append(post.views.count())
            labels.append(post.title)

    fig = go.Figure()
    fig.add_trace(go.Pie(labels = labels, values=values))
    fig = cleanse_fig(fig)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return HttpResponse(plot_div)





def fetch_aio_sensors(request):
    s = sensor.objects.using('aio_analytics').all()

    time = list(s.values_list("time", flat=True))
    h = list(s.values_list("humidity", flat=True))
    l = list(s.values_list("luminosity", flat=True))
    t = list(s.values_list("temperature", flat=True))

    fig = go.Figure()
    l = [100 * li for li in l]
    fig.add_trace(go.Scatter(x=time, y=l, name='luminosity', opacity=0.02, fill='tozeroy', mode='none', line_color='grey'))

    fig.add_trace(go.Scatter(x=time, y=h, mode='lines', name='humidity', opacity=0.8))
    fig.add_trace(go.Scatter(x=time, y=t, mode='lines', name='temperature', opacity=0.8))


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