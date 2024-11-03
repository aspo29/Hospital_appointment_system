# payment/urls.py
from django.urls import path
from . import views
app_name = 'payment'  # This sets the namespace
urlpatterns = [
    path('checkout/<int:patient_id>/<int:price>/', views.checkout, name='checkout'),
    path('successes/', views.success_view, name='success'),
    # Add other payment-related URLs here
]