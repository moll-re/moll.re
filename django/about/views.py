from django.shortcuts import render

# Create your views here.
def index(request):
    context = {"timeline" : generate_event_list()}
    return render(request, "about/base.html", context)


def generate_event_list():
    events = [
        {
            "date" : "01.05.2021",
            "title" : "Job at COSS",
            "link" : "https://coss.ethz.ch",
            "text" : "I am a student-assistant for prof. Dirk Helbing, assisting in various tasks relevant to his work."
        },
        {
            "date" : "01.09.2020",
            "title" : "Teaching assistant at D-INFK",
            "link" : "https://inf.ethz.ch",
            "text" : "During the semester I held a weekly tutorial accompagnying the lecure 'Informatik 1' held by prof. Friedrich and prof. Schwerhoff."
        },
        {
            "date" : "19.06.2019",
            "title" : "Franco-german baccaleaureate at the DFG/LFA",
            "link" : "https://dfglfa.net/dfg/de",
            "text" : "It is a binational diploma which I got with an NC. of 1.0 (mention très bien for the french equivalent)"
        }
    ]
    return events