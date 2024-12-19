from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('api/post-qr-data/', views.post_qr_data, name='post_qr_data'),
    path('qr/', views.qr_reader_view, name='qr_reader_view'),
    path('attenders/', views.list_attenders, name='list_attenders'),
    path('add-attender/', views.add_attender, name='add_attender'),
    path('attenders/<int:pk>/', views.attender_overview, name='attender_overview'),
    path('download-attendances/', views.download_attendances, name='download_attendances'),
    path('add-event/', views.add_event, name='add_event'),
    path('mail-code/<int:attender_id>/', views.send_qr_code_mail, name='mail_code'),
]
