from django.shortcuts import render
import markdown


# Create your views here.

def about(request):
    """This is the index view

    Renders the index template with the BuildingForm.
    """
    f = open("README.md", "r")
    f = f.read()

    # Replace ".templateapp" with an empty string for the images to load correctly in the webapp
    f = f.replace("./templateapp", "")

    html = markdown.markdown(f)
    context = {"html": html}
    return render(request, "templateapp/about.html", context)


def contact(request):
    """This is the index view

    Renders the index template with the BuildingForm.
    """
    context = {}
    return render(request, "templateapp/contact.html", context)


def impressum(request):
    """This is the index view

    Renders the index template with the BuildingForm.
    """
    context = {}
    return render(request, "templateapp/impressum.html", context)
