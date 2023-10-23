from django import forms
from django.utils.safestring import mark_safe
from bootstrap_datepicker_plus.widgets import DatePickerInput

datatype = forms.ChoiceField(
    choices=(
        ("CSV", "CSV (.csv)"),
        ("JSON", "JSON (.json)"),
        ("TMY3.MOS", "ReaderTMY3-Modelica (.mos)"),
        ("IWEC.EPW", "EnergyPlus (.epw)"),
        ("DATAFRAME.PICKLE", "pandas.Dataframe (.pickle)"),
    ),
    required=True,
)


class HistoricalForm(forms.Form):
    station_id = forms.CharField(
        max_length=10,
        required=False,
        initial="15000",
        label=mark_safe(
            'Station ID (<a href="https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/historical/TU_Stundenwerte_Beschreibung_Stationen.txt" target="_blank">ID List</a>)'
        ),
    )

    start_date = forms.DateField(widget=DatePickerInput(format="%Y-%m-%d"))

    end_date = forms.DateField(widget=DatePickerInput(format="%Y-%m-%d"))
    output_format = datatype

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")


class ForecastForm(forms.Form):
    station_id = forms.CharField(
        max_length=10,
        required=False,
        initial="10505",
        label=mark_safe(
            'Station ID (<a href="https://www.dwd.de/DE/leistungen/met_verfahren_mosmix/mosmix_stationskatalog.cfg?view=nasPublication&nn=16102" target="_blank">ID List</a>)'
        ),
    )
    output_format = datatype


class TRYForm(forms.Form):
    file = forms.FileField(label="Insert TRY.dat file  ", required=True)
    output_format = datatype


class EPWForm(forms.Form):
    file = forms.FileField(label="Insert EPW file  ", required=True)
    output_format = datatype


class ERCForm(forms.Form):
    start_date = forms.DateField(widget=DatePickerInput(format="%Y-%m-%d"))
    end_date = forms.DateField(widget=DatePickerInput(format="%Y-%m-%d"))
    output_format = datatype

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")
