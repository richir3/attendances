from django import forms
from django.forms import ModelForm
from .models import Attender, Event
import datetime

class EventForm(forms.Form):
    try:
        default_event = Event.objects.get(date=datetime.date.today())
    except:
        default_event = None
    try:
        evento = forms.ModelChoiceField(
            queryset=Event.objects.filter(date__gte=datetime.date.today()).order_by('date'), 
            initial=default_event, 
            required=True,
            empty_label="Seleccione un evento", 
            widget=forms.Select(
                attrs={"class": "form-control form-select", 
                    "id": "event-form",
                    "label": "Evento",
                    }
                )
            )
    except:
        pass

class AddEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre", "required": True, "autocomplete": "off", "label": "Nombre"}),
            'date': forms.DateInput(attrs={"class": "form-control", "placeholder": "Date", "required": True, "autocomplete": "off", "type": "date"}),
        }

class AttenderForm(ModelForm):
    class Meta:
        model = Attender
        fields = ['name', 'surname', 'brotherhood']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre", "required": True, "autocomplete": "off"}),
            'surname': forms.TextInput(attrs={"class": "form-control", "placeholder": "Sobrenombre", "required": True, "autocomplete": "off"}),
            'brotherhood': forms.Select(attrs={"class": "form-control form-select", "placeholder": "Hermandad", "required": True, "autocomplete": "off"}),
        }