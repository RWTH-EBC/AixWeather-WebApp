from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
import datetime
from django.utils.safestring import mark_safe
import pandas as pd


class InputForm(forms.Form):
    def __init__(self, *args, **kwargs):
            super(InputForm, self).__init__(*args, **kwargs)
            self.fields['start_date'].widget= DatePickerInput(
                    format='%Y-%m-%d',
                    options={
                        "defaultDate"   : (datetime.datetime.now()).strftime('%Y'),
                    }).start_of("id_range")
            self.fields['end_date'].widget= DatePickerInput(
                    format='%Y-%m-%d',
                    options={
                        "defaultDate"   : (datetime.datetime.now()).strftime('%Y-%m-%d'),
                        "format"        : "YYYY-MM-DD"
                        }   
                    ).end_of("id_range")
    source      = forms.ChoiceField(choices=(("DWD","DWD"),("ERC","ERC(Private)")), required=True)
    datatype    = forms.ChoiceField(choices=(("DATAFRAME.PICKLE","Pandas Dataframe"),("TMY3.MOS","Modelica"),("IWEC.EPW","EnergyPlus"), ("JSON", "JSON")), required=True)
    start_date  = forms.DateField(
            widget=DatePickerInput(
                format='%Y-%m-%d',
                options={
                    "defaultDate"   : (datetime.datetime.now()).strftime('%Y'),
                    }   
            ).start_of("id_range"))
    end_date    = forms.DateField(
            widget=DatePickerInput(
                format='%Y-%m-%d',
                options={
                    "defaultDate"   : (datetime.datetime.now()).strftime('%Y-%m-%d'),
                    "format"        : "YYYY-MM-DD"
                    }   
            ).end_of("id_range")
            )
    #utc = forms.BooleanField(widget=forms.widgets.CheckboxInput(attrs={'class': 'checkbox-inline'}), required=False, label= "Interpolate radiance?", help_text = "use hourly radiance point as middle point", initial=True)
    station_id  = forms.CharField(max_length=10, required=False, initial="15000", label=mark_safe('Station ID (<a href="https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/historical/TU_Stundenwerte_Beschreibung_Stationen.txt" target="_blank">ID List</a>)' ))
    comment1    = forms.CharField(max_length=200, required= False, label="Comment 1",widget=forms.Textarea)
    comment2    = forms.CharField(max_length=200, required= False, label="Comment 2",widget=forms.Textarea)
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date < start_date:
                raise forms.ValidationError("End date should be greater than start date.")

class ForecastForm(forms.Form):
    
    datatype    = forms.ChoiceField(choices=(("JSON","JSON Pickle"),("MOS","Modelica")), required=True)
    station_id  = forms.CharField(max_length=10, required=False, initial="10505", label=mark_safe('Station ID (<a href="https://www.dwd.de/DE/leistungen/met_verfahren_mosmix/mosmix_stationskatalog.cfg?view=nasPublication&nn=16102" target="_blank">ID List</a>)' ))
    
    
