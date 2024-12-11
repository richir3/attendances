from django.db import models
from django.contrib.auth.models import AbstractUser

class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name} - {self.date.strftime('%d/%m/%Y')}"

class Attender(models.Model):
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'This email is already in use.',
            'invalid': 'Enter a valid email address.',
        }
    )
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.surname}"

class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(Attender, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.event.name}"