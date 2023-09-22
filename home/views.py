from django.shortcuts import render

# Create your views here.


def index(request):
    """ A view to return the index page """

    template = 'home/index.html'
    return render(request, template)