pages = [
    {
        "name" : "Physics",
        "url" : "physics"
    },
    {
        "name" : "Anylytics",
        "url" : "analytics",
    },
    {
        "name" : "About",
        "url" : "about"
    }
]

def navlinks(request):
    page = request.path[1:] # remove leading /
    page = page[:page.find("/")]
    
    context = []
    for p in pages:
        p["active"] = p["url"] == page
        context.append(p)
    return {'navlinks': context}

