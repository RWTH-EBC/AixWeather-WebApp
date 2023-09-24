from django.shortcuts import render
from django.views.static import serve
from django.template import RequestContext

# Create your views here.

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

