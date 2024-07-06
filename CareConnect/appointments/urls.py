from django.urls import path
from . import views

urlpatterns = [
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('book-another-appointment/', views.book_another_appointment, name='book_another_appointment'),
    path('', views.appointment_list, name='appointment_list'),
    path('add/', views.add_appointment, name='add_appointment'),
    path('delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('update/<int:appointment_id>/', views.update_appointment, name='update_appointment'),
    path('success/<int:appointment_id>/', views.success_view, name='success_view'),
    path('ticket/', views.ticket, name='ticket'),
    path('ajax/get-specialty-by-doctor/', views.get_specialty_by_doctor, name='get_specialty_by_doctor'),
    path('ajax/get-doctor-by-specialty/', views.get_doctor_by_specialty, name='get_doctor_by_specialty'),
]
