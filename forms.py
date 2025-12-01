from django import forms
from .models import Reading

class ReadingForm(forms.ModelForm):
    class Meta:
        model = Reading
        fields = ("sensor_id", "temperature_c")
        widgets = {
            "sensor_id": forms.TextInput(attrs={"class": "form-control", "placeholder": "ID capteur"}),
            "temperature_c": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
        }
