pages = [
    {
        "name" : "Physics",
        "url" : "/physics"
    },
    {
        "name" : "Analytics",
        "url" : "/analytics",
    },
    {
        "name" : "About",
        "url" : "/about"
    }
]

def navlinks(request):
    page = request.path[1:] # remove leading /
    page = page[:page.find("/")]
    
    context = []
    for p in pages:
        p["active"] = p["url"][1:] == page
        context.append(p)
    return {'navlinks': context}

