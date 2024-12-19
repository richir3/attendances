from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'date']

class AttenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attender
        fields = ['name', 'surname', 'brotherhood', 'code']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class BrotherhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brotherhood
        fields = '__all__'