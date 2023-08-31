# -*- coding: future_fstrings -*-
import os
import datetime as dt
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from NewProgram.core.imports.ERC import load_credentials_ERC_weather_data
from .forms import InputForm, ForecastForm
from django.core.files.storage import FileSystemStorage
from timezonefinder import TimezoneFinder
from NewProgram import project_class

# Create your views here.
tzf = TimezoneFinder(in_memory=True)
fs = FileSystemStorage()


def index_view(request):
    if request.method == 'POST':
        forecast_form = ForecastForm(request.POST)
        form          =   InputForm(request.POST)
        if "forecast" in request.POST:
            # forecast
            station_id  =   form['station_id'].value()
            data_type   =   form['datatype'].value()
            response = download_forecast(station_id, data_type)
            return response
        if form.is_valid():
            # dwd weather historical data
            startdate   =   form['start_date'].value()
            starttime   =   dt.datetime.strptime((startdate+" 00:00"), '%Y-%m-%d %H:%M')
            enddate     =   form['end_date'].value()
            endtime     =   dt.datetime.strptime((enddate+" 00:00"), '%Y-%m-%d %H:%M') + dt.timedelta(days=1)
            station_id  =   form['station_id'].value()
            data_type   =   form['datatype'].value()
            comment_1   =   form['comment1'].value()
            comment_2   =   form['comment2'].value()
            source      =   form['source'].value()
            utc = True
            if "download" in request.POST:
                response = download_data(starttime, endtime, station_id, data_type, source, utc, comment_1, comment_2)
                return response
    else:
        form = InputForm()
        forecast_form = ForecastForm()
    context = {
        "form" : form,
        "forecast_form" : forecast_form
    }
    return render(request, 'converter/converterapp.html', context)



""""""
def download_data(start, stop, station, type, source, utc, comment1 = None, comment2 = None):

    '''
    function to download data depending on user's sepcifications

        Parameters:
            start:       (datetime obj)    data start
            stop:        (datetime obj)    data stop
            station:     (string/int)      station id
        Return:
            weatherfile
    '''

    if source != "ERC":
        data=project_class.project_class_DWD_Historical(start, stop, station)
        data.import_data()
        data.data_2_core_data()

    else:
        cred=load_credentials_ERC_weather_data()
        data=project_class.project_class_ERC(start, stop, cred)
        data.import_data()
        data.data_2_core_data()

    if type == "IWEC.EPW":
        data.core_2_epw()
        response=data.download_file(data.output_file_epw)
    elif type == "TMY3.MOS":
        data.core_2_mos()
        response=data.download_file(data.output_file_mos)
    elif type == "DATAFRAME.PICKLE":
        data.core_2_pickle()
        filename=data.output_file_pickle
        with open(filename, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attatchment; filename=' + os.path.basename(filename)
    elif type == "JSON":
        data.core_2_json()
        response = JsonResponse(data.output_df_json, safe=False)
    return response    
        


def download_forecast(station, type):
    '''
    function to download data depending on user's sepcifications
        Parameters:
            type:        (string)          type of data
        Return:
            forecast data
    '''
    data=project_class.project_class_DWD_Forecast()
    data.import_data(station)
    data.data_2_core_data()
    if type == "PICKLE":
        data.core_2_pickle()
        filename = data.output_file_pickle
        with open(filename, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attatchment; filename=' + os.path.basename(filename)
            return response
    elif type == "JSON":
        data.core_2_json()
        response = data.output_data_df_json
        return JsonResponse(response, safe=False)
    elif type == "MOS":
        filename = data.core_2_mos()
        return data.download_file(data.output_file_mos)

