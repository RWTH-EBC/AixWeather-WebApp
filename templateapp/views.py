from django.shortcuts import render
from django.views.static import serve
from django.template import RequestContext

# Create your views here.


def index(request):
    """This is the index view

    Renders the index template with the BuildingForm.
    """
    context = {}
    return render(request, 'templateapp/Index.html', context)
    

def progressurl(request):
    """This is the index view

    Renders the index template with the BuildingForm.
    """
    context = {}
    return render(request, 'templateapp/first_site.html', context)
    
def about(request):
    """This is the index view

    Renders the index template with the BuildingForm.
    """
    context = {}
    return render(request, 'templateapp/about.html', context)
    
def contact(request):
    """This is the index view

    Renders the index template with the BuildingForm.
    """
    context = {}
    return render(request, 'templateapp/contact.html', context)

def privacypolicy(request):
    """This is the index view

    Renders the index template with the BuildingForm.
    """
    context = {}
    return render(request, 'templateapp/privacypolicy.html', context)

def result(request):
    """This is the index view

    Renders the index template with the BuildingForm.
    """
    context = {}
    return render(request, 'templateapp/result.html', context)
