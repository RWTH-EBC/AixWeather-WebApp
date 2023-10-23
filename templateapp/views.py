from django.shortcuts import render
from django.views.static import serve
from django.template import RequestContext

# Create your views here.
import markdown

def about(request):
    """This is the index view

    Renders the index template with the BuildingForm.
    """
    f = open("README.md","r")
    f = f.read()

    # Replace ".templateapp" with an empty string for the images to load correctly in the webapp
    f = f.replace("./templateapp", "")

    html = markdown.markdown(f)
    context = {
        'html':html
    }
    return render(request, 'templateapp/about.html', context)
    
def contact(request):
    """This is the index view

    Renders the index template with the BuildingForm.
    """
    context = {}
    return render(request, 'templateapp/contact.html', context)



