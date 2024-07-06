from django.urls import path
from . import views

urlpatterns = [
path('list/', views.patient_list, name='patient_list'),
    path('delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('add/', views.add_patient, name='add_patient'), 
    path('update/<int:patient_id>/', views.update_patient, name='update_patient'),
]