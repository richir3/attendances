import json, random, openpyxl, datetime, base64, qrcode
from openpyxl.styles import Font, Alignment
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Attender, Event, Attendance
from .forms import AttenderForm, EventForm, AddEventForm
from io import BytesIO
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.
@login_required
def home(request):

    class Functionality:
        def __init__(self, name, url):
            self.name = name
            self.url = url

        def __repr__(self):
            return f"{self.name.lower().replace(' ', '-')}"

    functionalities = [
        Functionality("QR Reader", reverse("qr_reader_view")),
        Functionality("List Attenders", reverse("list_attenders")),
        Functionality("Add Event", reverse("add_event")),
    ]
    
    return render(request, "home.html", {"functionalities": functionalities})

@login_required
def qr_reader_view(request):
    codes = dict()
    for a in Attender.objects.all():
        codes[a.code] = a.name + " " + a.surname

    form = EventForm()
    return render(request, "reader.html", {"form": form, "codes": codes})

@login_required
def post_qr_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        # return JsonResponse({"message": "Data saved!"}, status=200)

        try:
            attender = Attender.objects.get(code=data['content'])  
            event = Event.objects.get(id=data['date'])
            # come faccio a sapere se Attendance.objects.get(event=event, user=attender) esiste nel mio db?
            if Attendance.objects.filter(event=event, user=attender).exists():
                response = JsonResponse({'status': 'error', 'error': 'Attender already attended to the event'}, status=400)
            else:
                print("Creating attendance")
                attendance = Attendance(event=event, user=attender)
                attendance.save()
                response = JsonResponse({'status': 'success', 'message': 'Attendance saved'}, status=200)
        except KeyError as e:
            response = JsonResponse({'status': 'error', 'error': 'Invalid data'}, status=400)
        except Attender.DoesNotExist as e:
            response = JsonResponse({'status': 'error', 'error': 'Attender not found'}, status=404)
        except Event.DoesNotExist as e:
            response = JsonResponse({'status': 'error', 'error': 'Event not found'}, status=404)
        except json.JSONDecodeError as e:
            response = JsonResponse({'status': 'error', 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            response = JsonResponse({'status': 'error', 'error': str(e)}, status=500)
        finally:
            return response
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def list_attenders(request):    
    class AttenderShow:
        def __init__(self, attender):
            self.attender = attender
            self.attendances = Attendance.objects.filter(user=attender).count()
        
        def __repr__(self):
            return f"{self.attender.name} {self.attender.surname} - {self.attendances}"
    
    attenders = [AttenderShow(a) for a in Attender.objects.all()]

    context = {
        "attenders": attenders,
    }
    return render(request, "attenders.html", context=context)

@login_required
def add_attender(request):
    def create_code():
        codes = [attender.code for attender in Attender.objects.all()]
        code = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=10))
        while code in codes:
            code = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=10))
        return code

    if request.method == "POST":
        form = AttenderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            email = form.cleaned_data["email"]
            code = create_code()
            attender = Attender(
                name=name, 
                surname=surname, 
                email=email, 
                code=code, 
                email_verified=False
            )
            attender.save()
            return redirect("list_attenders")
    else:
        form = AttenderForm()
        return render(request, "add_attender.html", {"form": form})
# commento

@login_required
def attender_overview(request, pk):
    attender = Attender.objects.get(pk=pk)
    context = {
        "attender": attender,
        "events" : Event.objects.all(),
        "attendances" : [a.event for a in Attendance.objects.all().filter(user=attender)]
    }
    print(context)

    return render(request, "attender.html", context=context)

@login_required
def download_attendances(request):
    events = Event.objects.all().order_by("date")
    event_dates = [e.date.strftime("%d/%m/%Y") for e in events]

    attenders = Attender.objects.all()

    data = {}
    for a in attenders:
        data[a] = []
        for e in events:
            #if a.events.filter(pk=e.pk).exists():
            if Attendance.objects.filter(event=e, user=a).exists():
                data[a].append("YES")
            else:
                data[a].append("NO")

    df = pd.DataFrame(data).T
    df.columns = event_dates

    # insert a column in the dataframe with the total attendances, in the second position
    df.insert(0, "Total", df.apply(lambda x: x.value_counts().get("YES", 0), axis=1))

    # Creazione di un buffer in memoria
    buffer = BytesIO()

    # Scrittura iniziale del DataFrame in un file Excel
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=True, sheet_name="Attendances")

    # Caricamento del file Excel in openpyxl per le modifiche
    buffer.seek(0)  # Riavvolgi il buffer per leggerlo da openpyxl
    wb = openpyxl.load_workbook(buffer)
    ws = wb.active  # Seleziona il primo foglio

    # Modifiche al foglio di lavoro
    
    # imposta la prima riga come tipo data
    for cell in ws[1][1:]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")
        cell.number_format = "DD/MM/YYYY"
    
    # imposta le celle con YES in verde e quelle con NO in rosso
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=2, max_col=ws.max_column):
        for cell in row:
            if cell.value == "YES":
                cell.fill = openpyxl.styles.PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
            elif cell.value == "NO":
                cell.fill = openpyxl.styles.PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

    # adatta la larghezza delle colonne
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    # Scrivi le modifiche nel buffer
    new_buffer = BytesIO()  # Nuovo buffer per la risposta finale
    wb.save(new_buffer)
    new_buffer.seek(0)

    # Configura la risposta HTTP per il download del file
    response = HttpResponse(
        new_buffer,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    datefile = datetime.datetime.now().strftime("%d-%m-%Y--%H:%M")

    response["Content-Disposition"] = f'attachment; filename="asistencia_{datefile}.xlsx"'
    return response

@login_required
def add_event(request):
    if request.method == "POST":
        form = AddEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = AddEventForm()
        context = {
            "form": form,
            "events": Event.objects.filter(date__gte=datetime.date.today())
        }
        return render(request, "add_event.html", context)

@login_required
def send_email(request):
    subject = "Subject"
    message = "Message"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ["roxierba@gmail.com"]
    mail = EmailMessage(subject, message, email_from, recipient_list)
    mail.send()
    return HttpResponse("Email sent")

@login_required
def send_qr_code_mail(request, attender_id):
    if request.method == "POST":
        attender = Attender.objects.get(id=attender_id)

        # generate qr
        code = attender.code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(code)
        qr.make(fit=True)

        # Converti il QR Code in un'immagine PNG
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Codifica l'immagine in base64
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        context = {
            "attender": attender,
            "qr": img_base64,
        }

        print(context)

        # Render del template
        html_content = render_to_string("email/qr_email.html", context=context)
        text_content = strip_tags(html_content)  # Versione plain text
        
        # Configura la mail
        email = EmailMultiAlternatives(
            subject="Il tuo codice QR per l'evento",
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[attender.email],
        )

        # Invia la mail
        email.attach_alternative(html_content, "text/html")
        email.send()

        return JsonResponse({"status": "success", "message": "Email sent"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
