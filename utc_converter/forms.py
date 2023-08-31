from email.policy import default
from django import forms
from django.core.exceptions import ValidationError

class customFileForm(forms.Form):
    city = forms.CharField()
    file = forms.FileField(help_text="insert .pkl/.csv file here.",required=True)
    datatype    = forms.ChoiceField(choices=(("DATAFRAME.PICKLE","Pandas Dataframe"),("TMY3.MOS","Modelica"),("IWEC.EPW","EnergyPlus"), ("JSON", "JSON")), required=True)

class TRYFileForm(forms.Form):
    city = forms.CharField()
    file = forms.FileField(help_text="insert TRY.dat file here.",required=True)
    datatype    = forms.ChoiceField(choices=(("DATAFRAME.PICKLE","Pandas Dataframe"),("TMY3.MOS","Modelica"),("IWEC.EPW","EnergyPlus"), ("JSON", "JSON")), required=True)
