from django.urls import path
from . import views
from appointments.views import update_appointment, delete_appointment 

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('appointment/update/<int:appointment_id>/', update_appointment, name='update_appointment'),
    path('appointment/delete/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
    path('delete_account/', views.delete_account, name='delete_account'),
]
