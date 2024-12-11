from django import forms
from django.forms import ModelForm
from .models import Attender, Event
import datetime

class EventForm(forms.Form):
    default_event = Event.objects.filter(date__gte=datetime.date.today()).first()
    event = forms.ModelChoiceField(
        queryset=Event.objects.filter(date__gte=datetime.date.today()), 
        initial=default_event, 
        required=True,
        empty_label="Select an event", 
        widget=forms.Select(
            attrs={"class": "form-control", 
                   "id": "event-form"
                }
            )
        )
    
class AddEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Name", "required": True, "autocomplete": "off"}),
            'date': forms.DateInput(attrs={"class": "form-control", "placeholder": "Date", "required": True, "autocomplete": "off", "type": "date"}),
        }

class AttenderForm(ModelForm):
    class Meta:
        model = Attender
        fields = ['name', 'surname', 'email']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Name", "required": True, "autocomplete": "off"}),
            'surname': forms.TextInput(attrs={"class": "form-control", "placeholder": "Surname", "required": True, "autocomplete": "off"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email", "required": True, "autocomplete": "off"}),
        }

class AttenderUpdateForm(ModelForm):
    class Meta:
        model = Attender
        fields = ['name', 'surname', 'email']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Name", "required": True, "autocomplete": "off"}),
            'surname': forms.TextInput(attrs={"class": "form-control", "placeholder": "Surname", "required": True, "autocomplete": "off"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email", "required": True, "autocomplete": "off"}),
        }