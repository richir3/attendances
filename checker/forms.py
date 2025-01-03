from django import forms
from django.forms import ModelForm
from .models import Attender, Event
import datetime

class EventForm(forms.Form):
    evento = forms.ModelChoiceField(
            queryset=Event.objects.all().order_by('date'), 
            initial=Event.objects.get(date=datetime.date.today()), 
            required=True,
            empty_label="Seleccione un evento", 
            widget=forms.Select(
                attrs={"class": "form-control form-select", 
                    "id": "event-form",
                    "label": "Evento",
                    }
                )
            )

class AddEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre", "required": True, "autocomplete": "off", "label": "Nombre"}),
            'date': forms.DateInput(attrs={"class": "form-control", "placeholder": "Date", "required": True, "autocomplete": "off", "type": "date"}),
        }

class AttenderForm(ModelForm):
    COFRADIA = 'Selecciona una cofradía'

    class Meta:
        model = Attender
        fields = ['name', 'surname', 'brotherhood']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre", "required": True, "autocomplete": "off"}),
            'surname': forms.TextInput(attrs={"class": "form-control", "placeholder": "Sobrenombre", "required": True, "autocomplete": "off"}),
            'brotherhood': forms.Select(attrs={"class": "form-control form-select", "empty_label": "Hermandad", "required": True, "autocomplete": "off"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brotherhood'].empty_label = self.COFRADIA


class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email", "required": True, "autocomplete": "off"}
        )
    )
