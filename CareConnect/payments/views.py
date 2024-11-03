# from django.shortcuts import render

# Create your views here.
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from patients.models import Patient  # Adjust this import to match your actual models
from .models import  Payment
from appointments.models import Appointment
from django.contrib import messages
from django.utils.crypto import get_random_string
from .signature import generate_signature
import uuid
from django.urls import reverse
import base64
import requests
from django.http import HttpResponseBadRequest
import json

def checkout(request, patient_id, price):
    patient = get_object_or_404(Patient, id=patient_id)
    transaction_uuid = uuid.uuid4()  # Generate a unique transaction ID
    tax_amount = 10  # You can adjust tax or add more charges if needed
    total_amount = price + tax_amount  # Total price including tax
    secret_key = '8gBm/:&EnhH.1/q'
    data_to_sign = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code=EPAYTEST"
    result = generate_signature(secret_key, data_to_sign)
    payment = Payment.objects.first() 
    payment_code = payment.code if payment else 'EPAYTEST'
    # Prepare data for the checkout page
    context = {
        'patient': patient,
        'price':price,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'transaction_uuid': transaction_uuid,
        'payment_code': payment_code,
        'product_delivery_charge': 0,
        'product_service_charge': 0,
        'signature': result,
    }

    # Render the checkout page with payment details
    return render(request, 'payments/checkout.html', context)

def success_view(request):
    context = {}  # Create a dictionary to store the response

    # Get the base64 encoded data from the URL parameters
    data = request.GET.get('data')
    if not data:
        return HttpResponseBadRequest("Missing data parameter.")

    try:
        # Decode the base64 encoded data
        decoded_data = base64.b64decode(data).decode('utf-8')
        data_dict = json.loads(decoded_data)  # Convert the data to a dictionary

        # Retrieve the Payment object by unique criteria (like patient_name or code)
        patient_code = data_dict['product_code']
        payment = get_object_or_404(Payment, code=patient_code)  # Adjust criteria as needed

        # Access the appointment ID directly
        appointment_id = payment.appointment.id

        # Get the required values from the dictionary
        total_amount = data_dict['total_amount']
        transaction_uuid = data_dict['transaction_uuid']
        # patient_code = data_dict['product_code']  # Make sure this is present

        # Make a request to the eSewa API to check the transaction status
        request_url = f'https://uat.esewa.com.np/api/epay/transaction/status/?product_code={patient_code}&total_amount={total_amount}&transaction_uuid={transaction_uuid}'
        response = requests.get(request_url)
        response = json.loads(response.text)
        
        # Put the Status in message key of the context dictionary
        context['message'] = response['status']
        print(context)

    except (ValueError, json.JSONDecodeError) as e:
        return HttpResponseBadRequest("Invalid data received.")
    except Exception as e:
        return HttpResponseBadRequest(f"An error occurred: {str(e)}")

    # Clear any session data related to the appointment form
    request.session.pop('appointment_form_data', None)
    request.session.pop('patient_form_data', None)
    # Redirect to the success view with the appointment ID in the URL
    messages.success(request, 'Appointment created successfully. You will soon be contacted by the hospital.')
    return redirect(reverse('appointment:success_view', args=[appointment_id]))