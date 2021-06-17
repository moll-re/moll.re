from django.shortcuts import render

def index(request):
    context = {}
    return render(request, "home/base.html", context)
