# -*- coding: future_fstrings -*-
import os
import datetime as dt
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import HistoricalForm, ForecastForm, TRYForm, EPWForm, ERCForm
from aixweather import project_class
import config
from converter.utils import handle_uploaded_file, plot_heatmap_missing_values_daily
import shutil
from pathlib import Path
# Create your views here.

def index_view(request):
    if request.method == 'POST':

        if "forecast" in request.POST or "forecast_quality_check" in request.POST:
            # forecast
            quality_check   =   False
            forecast_form   =   ForecastForm(request.POST)
            station_id      =   forecast_form['station_id'].value()
            data_type       =   forecast_form['output_format'].value()
            if "forecast_quality_check" in request.POST:
                quality_check=True
            response        =   download_forecast(request,station_id, data_type,quality_check)
        elif "historical" in request.POST or "historical_quality_check" in request.POST:
            # dwd weather historical data
            quality_check   =   False
            historical_form =   HistoricalForm(request.POST)
            startdate       =   historical_form['start_date'].value()
            starttime       =   dt.datetime.strptime((startdate+" 00:00"), '%Y-%m-%d %H:%M')
            enddate         =   historical_form['end_date'].value()
            endtime         =   dt.datetime.strptime((enddate+" 00:00"), '%Y-%m-%d %H:%M') + dt.timedelta(days=1)
            station_id      =   historical_form['station_id'].value()
            data_type       =   historical_form['output_format'].value()
            if "historical_quality_check" in request.POST:
                quality_check=True
            response = download_historical(request,starttime, endtime, station_id, data_type,quality_check)

        elif "try" in request.POST or "try_quality_check" in request.POST:
            quality_check   =   False
            try_form        =   TRYForm(request.POST)
            data_type       =   try_form['output_format'].value()
            path            =   handle_uploaded_file(request.FILES['file'])
            if "try_quality_check" in request.POST:
                quality_check=True
            response=download_try(request,path,data_type,quality_check)

        elif "epw" in request.POST or "epw_quality_check" in request.POST:
            quality_check   =   False
            epw_form    =   EPWForm(request.POST)
            data_type   =   epw_form['output_format'].value()
            path        =   handle_uploaded_file(request.FILES['file'])
            if "epw_quality_check" in request.POST:
                quality_check=True
            response    =   download_epw(request,path,data_type,quality_check)

        elif "erc" in request.POST or "erc_quality_check" in request.POST:
            quality_check   =   False
            erc_form    =   ERCForm(request.POST)
            startdate   =   erc_form['start_date'].value()
            starttime   =   dt.datetime.strptime((startdate+" 00:00"), '%Y-%m-%d %H:%M')
            enddate     =   erc_form['end_date'].value()
            endtime     =   dt.datetime.strptime((enddate+" 00:00"), '%Y-%m-%d %H:%M') + dt.timedelta(days=1)
            data_type   =   erc_form['output_format'].value()
            if "erc_quality_check" in request.POST:
                quality_check=True
            response=download_erc(request,starttime,endtime,(config.username,config.password),data_type,quality_check)
        return response     
    else:
        historical_form = HistoricalForm()
        forecast_form   = ForecastForm()
        try_form        = TRYForm()
        epw_form        = EPWForm()
        erc_form        = ERCForm()
    context = {
        "historical_form" : historical_form,
        "forecast_form" : forecast_form,
        "try_form" : try_form,
        "epw_form" : epw_form,
        "erc_form" : erc_form,
    }
    return render(request, 'converter/converterapp.html', context)




def download_historical(request, start, stop, station, type, quality_check):

    '''
    function to download data depending on user's sepcifications

        Parameters:
            start:       (datetime obj)    data start
            stop:        (datetime obj)    data stop
            station:     (string/int)      station id
            type:        (string/int)      type of output weatherfile
        Return:
            weatherfile
    '''
    if quality_check:
        DWD_data = project_class.ProjectClassDWDHistorical(start,stop,station)
        return quality_check_function(request,DWD_data=DWD_data)
    else:
        i = 0
        while os.path.exists("results\data%s\data%s" % (i, i)):
            i += 1
        os.makedirs("results\data%s\data%s" % (i, i))
        DWD_data = project_class.ProjectClassDWDHistorical(start,stop,station,abs_result_folder_path="results\data%s\data%s" % (i, i))
        return handle_output(DWD_data,type)  
            


def download_forecast(request, station, type, quality_check):
    '''
    function to download data depending on user's sepcifications
        Parameters:
            station:     (string/int)      station id
            type:        (string)          type of data
        Return:
            forecast data
    '''
    if quality_check:
        DWD_data = project_class.ProjectClassDWDForecast(station)
        return quality_check_function(request,DWD_data=DWD_data)
    else:
        i = 0
        while os.path.exists("results\data%s\data%s" % (i, i)):
            i += 1
        os.makedirs("results\data%s\data%s" % (i, i))
        DWD_data = project_class.ProjectClassDWDForecast(station,abs_result_folder_path="results\data%s\data%s" % (i, i))
        return handle_output(DWD_data,type)



def download_try(rquest, path, type, quality_check):
    '''
    function to download data depending on user's sepcifications
        Parameters:
            path:        (path)            path to try.dat file
            type:        (string)          type of output weatherfile
        Return:
            weatherfile
    '''
    if quality_check:
        DWD_data = project_class.ProjectClassTRY(path)
        return quality_check_function(request,DWD_data=DWD_data)
    else:
        i = 0
        while os.path.exists("results\data%s\data%s" % (i, i)):
            i += 1
        os.makedirs("results\data%s\data%s" % (i, i))
        DWD_data = project_class.ProjectClassTRY(path,abs_result_folder_path="results\data%s\data%s" % i % i)
        return handle_output(DWD_data,type)  

def download_epw(request, path, type, quality_check):
    '''
    function to download data depending on user's sepcifications
        Parameters:
            path:        (path)            path to .epw file
            type:        (string)          type of output weatherfile
        Return:
            weatherfile
    '''
    if quality_check:
        DWD_data = project_class.ProjectClassEPW(path)
        return quality_check_function(request,DWD_data=DWD_data)
    else:
        i = 0
        while os.path.exists("results\data%s\data%s" % (i, i)):
            i += 1
        os.makedirs("results\data%s\data%s" % (i, i))
        DWD_data = project_class.ProjectClassEPW(path,abs_result_folder_path="results\data%s\data%s" % (i, i))
        return handle_output(DWD_data,type)

def download_erc(request, start, stop, cred, type, quality_check):
    '''
    function to download data depending on user's sepcifications

        Parameters:
            start:       (datetime obj)    data start
            stop:        (datetime obj)    data stop
            cred:        (tuple)           ERC credentials
            type:        (string/int)      type of output weatherfile
        Return:
            weatherfile
    '''
    if quality_check:
        DWD_data = project_class.ProjectClassERC(start,stop,cred)
        return quality_check_function(request,DWD_data=DWD_data)
    else:
        i = 0
        while os.path.exists("results\data%s\data%s" % (i, i)):
            i += 1
        os.makedirs("results\data%s\data%s" % (i, i))
        DWD_data = project_class.ProjectClassERC(start,stop,cred,abs_result_folder_path="results\data%s\data%s" % (i, i))
        return handle_output(DWD_data,type)



def handle_output(DWD_data,type):
    DWD_data.import_data()
    DWD_data.data_2_core_data()
    if type == "IWEC.EPW":
        DWD_data.core_2_epw()
    elif type == "TMY3.MOS":
        DWD_data.core_2_mos()
    elif type == "DATAFRAME.PICKLE":
        DWD_data.core_2_pickle()  
    elif type == "JSON":
        DWD_data.core_2_json()
    else:
        DWD_data.core_2_csv()
    path=Path(DWD_data.abs_result_folder_path).parent
    shutil.make_archive(os.path.join(path,'weatherdata'), 'zip', DWD_data.abs_result_folder_path)
    filename=os.path.join(path,'weatherdata.zip')
    with open(filename, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attatchment; filename=' + os.path.basename(filename)
    shutil.rmtree(path, ignore_errors=True)
    return response


def quality_check_function(request,DWD_data):

    DWD_data.import_data()
    DWD_data.data_2_core_data()
    graph = plot_heatmap_missing_values_daily(DWD_data.core_data)

    # Render the graph to the template
    return render(request, 'converter/quality_check.html', {'graph': graph})


