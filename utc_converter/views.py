from django.shortcuts import render
import os
import pandas as pd
from .forms import customFileForm, TRYFileForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from NewProgram import project_class
# Create your views here.
def index_view(request):
    if request.method == 'POST':
        if "custom" in request.POST:
            form = customFileForm(request.POST)   
        elif "try" in request.POST:
            form = TRYFileForm(request.POST)
        path = handle_uploaded_file(request.FILES['file'])
        loc = form['city'].value()
        data_type   =   form['datatype'].value()
        return utc_convert(path, loc, data_type)

    context= {
        'customForm' : customFileForm(),
        'tryForm'    : TRYFileForm(),
    }
    return render(request, 'utc_converter/utc_converter.html', context)

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


def utc_convert(path, loc, data_type): 
    '''
    convert uploaded file into UTC mos file
        Parameters:
            path: (string) path to file
            loc: (string/int) location of station        
        Return:
            weather file
    '''
    
    if path.endswith(".pkl"):
        weatherdata = pd.read_pickle(path)
        src="converted PICKLE source"
    elif path.endswith(".csv"):
        weatherdata = pd.read_csv(path, index_col=0)
        src="converted CSV source"
    elif path.endswith(".dat"):
        weatherdata=project_class.project_class_TRY(loc) 
        weatherdata.import_data(path)
        src="converted TRY source"
        # df from TRY at this point already at indicated time and UTC
    else:
        return HttpResponse("Wrong File Format!", status=200)
    # set index to datetime index
    weatherdata.imported_data.index = pd.to_datetime(weatherdata.imported_data.index)
    weatherdata.imported_data.index.name = "timestamp"
    weatherdata.data_2_core_data(weatherdata.imported_data.index[0], weatherdata.imported_data.index[-1])
    if data_type == "IWEC.EPW":
        weatherdata.core_2_epw()
        filename = weatherdata.output_file_epw
    elif data_type == "TMY3.MOS":
        weatherdata.core_2_mos(src)
        filename = weatherdata.output_file_mos
    elif data_type == "DATAFRAME.PICKLE":
        weatherdata.core_2_pickle()
        filename = weatherdata.output_file_pickle
        with open(filename, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attatchment; filename=' + os.path.basename(filename)
            return response
    elif data_type == "JSON":
        weatherdata.core_2_json(orient="columns")
        f=weatherdata.output_df_json
        response = JsonResponse(f, safe=False)
        return response
    return weatherdata.download_file(filename)





    