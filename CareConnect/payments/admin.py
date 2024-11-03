from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_name', 'price', 'code', 'timestamp', 'success')  # Customize fields as needed
    list_filter = ('timestamp', 'success')  # Filter by timestamp and success
    search_fields = ('patient_name', 'code')  # Search by patient name and code
    ordering = ('-timestamp',)  # Order by timestamp in descending order

    fieldsets = (
        (None, {
            'fields': ('patient_name', 'price', 'code', 'success')  # Add all relevant fields here
        }),
    )

# Register the Payment model with the PaymentAdmin configuration
admin.site.register(Payment, PaymentAdmin)