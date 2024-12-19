from django.db import models
import random

class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.date.strftime('%d/%m/%Y')}"

    def __repr__(self) -> str:
        return f"{self.date.strftime('%d/%m/%Y')}"

class Attender(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'surname'], name='unique_name_surname')
        ]

    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True, blank=True)
    brotherhood = models.ForeignKey('Brotherhood', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
    
    def save(self, *args, **kwargs):
        def create_code():
            codes = [attender.code for attender in Attender.objects.all()]
            code = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=10))
            while code in codes:
                code = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=10))
            return code
        if not self.code:
            self.code = create_code()
        super(Attender, self).save(*args, **kwargs)



class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(Attender, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.event.name}"
    
class Brotherhood(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'This email is already in use.',
            'invalid': 'Enter a valid email address.',
        }
    )

    def __str__(self):
        return self.name