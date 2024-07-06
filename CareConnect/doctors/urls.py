from django.urls import path
from . import views

urlpatterns = [
   path('find_doctors/<int:speciality_id>/', views.find_doctors, name='find_doctors_by_speciality'),
    path('find-doctors/', views.find_doctors, name='find_doctors'),
    path('list/', views.doctor_list, name='doctor_list'), 
    path('delete/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('add/', views.add_doctor, name='add_doctor'),  
    path('update/<int:doctor_id>/', views.update_doctor, name='update_doctor'), 
]
