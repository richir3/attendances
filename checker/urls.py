from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/post-qr-data/', views.post_qr_data, name='post_qr_data'),
    path('qr/', views.qr_reader_view, name='qr_reader_view'),
    path('attenders/', views.list_attenders, name='list_attenders'),
    path('add-attender/', views.add_attender, name='add_attender'),
    path('attenders/<int:pk>/', views.attender_overview, name='attender_overview'),
    path('attenders/<int:pk>/edit/', views.AttenderUpdateView.as_view(), name='attender_edit'),
    path('attenders/<int:pk>/delete/', views.AttenderDeleteView.as_view(), name='attender_delete'),
    path('download-attendances/', views.download_attendances, name='download_attendances'),
    path('add-event/', views.add_event, name='add_event'),
    path('events/', views.list_events, name='list_events'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_details'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('mail-code/<int:attender_id>/', views.send_qr_code_mail, name='mail_code'),
    path('mail-code-specific/<int:attender_id>/', views.send_qr_code_mail, name='mail_code_specific'),


    

    # rest api
    path('attenders-api/', views.AttenderListCreate.as_view(), name='attender-list'),
    path('attenders-api/<int:pk>/', views.AttenderRetrieveUpdateDestroy.as_view(), name='attender-detail'),
    path('events-api/', views.EventListCreate.as_view(), name='event-list'),
    path('events-api/<int:pk>/', views.EventRetrieveUpdateDestroy.as_view(), name='event-detail'),
    path('attendances-api/', views.AttendanceListCreate.as_view(), name='attendance-list'),
    path('attendances-api/<int:pk>/', views.AttendanceRetrieveUpdateDestroy.as_view(), name='attendance-detail'),
    path('brotherhoods-api/', views.BrotherhoodListCreate.as_view(), name='brotherhood-list'),
    path('brotherhoods-api/<int:pk>/', views.BrotherhoodRetrieveUpdateDestroy.as_view(), name='brotherhood-detail'),
]
