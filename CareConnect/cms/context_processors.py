from .models import StaticFile

def logo_processor(request):
    logo = StaticFile.objects.filter(name='logo').first()
    return {
        'logo': logo,
    }