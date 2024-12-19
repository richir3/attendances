from django.contrib import admin
from .models import *

# Register your models here.
# use the advanced way to show the models in the admin panel

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1

class EventAdmin(admin.ModelAdmin):
    inlines = [AttendanceInline]

admin.site.register(Attendance)
admin.site.register(Event, EventAdmin)
admin.site.register(Attender)
admin.site.register(Brotherhood)

