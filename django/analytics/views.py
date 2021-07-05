from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum, Count, Q
from django.db.models.functions import Trunc

import time

from physics.models import Post as ppost
# from blog.models import Post as bpost
post_list = [ppost]

from .models import SensorMetric as sensor
from .models import ChatMetric as chat
from .models import AIOList as alist


import plotly.graph_objects as go
from plotly.offline import plot
from plotly.graph_objs import Scatter

import datetime

card_str = """
<div class="card-body">
    <h5 class="card-title">{title}</h5>
    {content}
</div>
"""

delta = datetime.timedelta(days=7)
# used for setting the plot-range

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

    if request.user.is_authenticated:
        context["card_list"].append({
            "content": async_card(
                "Sensor metrics",
                "aio_sensors",
                "fetch_aio_sensors"
                ),
            "width" : 4})

        context["card_list"].append({
            "content": async_card(
                "Chat metrics",
                "aio_bot_stats",
                "fetch_aio_bot_stats"
                ),
            "width" : 4})

        context["card_list"].append({
            "content": async_card(
                "List content",
                "aio_lists",
                "fetch_aio_lists"
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
    fig = cleanse_fig(fig)
    fig.layout.update(
        xaxis = dict(range=[hours[-1] - delta, hours[-1]])
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
    fig.layout.update(
        xaxis = dict(range = [time[-1]-delta, time[-1]])
    )
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return HttpResponse(plot_div)



def get_cumulated():
    total_posts = 0
    total_views = 0
    for plist in [ppost]:
        total_posts += plist.objects.count()
        views = plist.objects.all().aggregate(Sum("views"))
        total_views += views["views__sum"]
    return total_posts, total_views



def fetch_aio_bot_stats(request):
    c = chat.objects.using('aio_analytics').all()

    
    hourly = c\
        .annotate(hour=Trunc('time', 'hour'))\
        .values('hour')\
        .annotate(call=Count('read', filter=Q(read=True)))
    
    hr = list(hourly.values_list("hour", flat=True))
    ar = list(hourly.values_list("call", flat=True))

    hourly = c\
        .annotate(hour=Trunc('time', 'hour'))\
        .values('hour')\
        .annotate(call=Count('send', filter=Q(send=True)))
    
    hs = list(hourly.values_list("hour", flat=True))
    a_s = list(hourly.values_list("call", flat=True))

    hourly = c\
        .annotate(hour=Trunc('time', 'hour'))\
        .values('hour')\
        .annotate(call=Count('execute', filter=Q(execute=True)))
    
    he = list(hourly.values_list("hour", flat=True))
    ae = list(hourly.values_list("call", flat=True))

    fig = go.Figure()
    
    fig.add_trace(go.Bar(x=hr, y=ar, name="received"))
    fig.add_trace(go.Bar(x=hs, y=a_s, name="sent"))
    fig.add_trace(go.Bar(x=he, y=ae, name="executed"))

    fig = cleanse_fig(fig)
    last_hour = max([hr[-1], hs[-1], he[-1]])
    fig.layout.update(
        xaxis = dict(range = [last_hour - delta, last_hour])
    )

    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return HttpResponse(plot_div)





list_base = """
<ul class='list-group list-group-flush'>
{}
</ul>
"""

def fetch_aio_lists(request):
    lists = alist.objects.using("aio_analytics").all()
    content = ""
    for l in list(lists):
        
        it = l.content.split("<-->")
        for i in it[:-1]:
            content += "<li class='list-group-item'>{}</li>\n".format(i)
    list_div = list_base.format(content)
    return HttpResponse(list_div)

######## helper:
def cleanse_fig(fig):
    fig.layout.update(
            xaxis = {
                'showgrid': False, # thin lines in the background
                # 'zeroline': False, # thick line at x=0
                # 'visible': False,  # numbers below
            }, # the same for yaxis
            yaxis = {
                'showgrid': False, # thin lines in the background
                # 'zeroline': False, # thick line at x=0
                # 'visible': False,  # numbers below
            }, # the same for yaxis

            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            )
    return fig