from django.urls import path
from . import views
from .views import HomeView

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', HomeView.as_view(), name='home'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('about-us/', views.about_us, name='about_us'),
    path('login/', views.login, name='login'),
    path('logout/user/', views.logout_user, name='logout_user'),
    path('logout/admin/', views.logout_admin, name='logout_admin'),
    path('register/', views.register, name='register'),  
    path('specialty/', views.specialty_list, name='specialty_list'),
    path('specialty/add/', views.add_specialty, name='add_specialty'),
    path('specialty/update/<int:specialty_id>/', views.update_specialty, name='update_specialty'),
    path('specialty/<int:specialty_id>/delete/', views.delete_specialty, name='delete_specialty'),
]
