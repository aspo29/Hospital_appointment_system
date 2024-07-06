from django.contrib import admin
from django.utils.safestring import mark_safe 
from .models import Doctor
# Register your models here.
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mobile', 'profession', 'image_tag')  
    search_fields = ('name', 'profession')
    list_filter = ('profession',)
    readonly_fields = ('image_tag',) 
    
    def image_tag(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" style="height: 50px; width:50px;" />'.format(obj.image.url))
        else:
            return None

    image_tag.short_description = 'Image Preview' 
