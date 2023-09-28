from django.core.files.storage import FileSystemStorage
import matplotlib.pyplot as plt
from io import BytesIO,StringIO
import base64
import seaborn as sns
import os


fs = FileSystemStorage()
# Function to handle data upload
def handle_uploaded_file(f):
    '''
    Import file and return the path to file, at the same time delete older file
        Parameter:
            f: (file)
        Return
            path
    '''
    fs = FileSystemStorage()
    path = os.path.join(fs.location, f.name)
    for file in fs.listdir(fs.location)[1]:
            if file:
                fs.delete(file)

    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return path

#Function plotly to rend graph to html supported format
def render_graph (plt):

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())


    return string.decode('utf-8')
