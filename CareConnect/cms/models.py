from django.db import models,connection


class Speciality(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField()
    image = models.ImageField(upload_to='specialty_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Profession(models.Model):
    name = models.CharField(max_length=100)  
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MedicalService(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField()
    image = models.ImageField(upload_to='services/')
    badge = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.name

class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel/')
    interval = models.IntegerField(default=4000)  # Default interval of 4000ms

    def __str__(self):
        return f"Carousel Image {self.id}"
    
class StaticFile(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='static_files/')

    def __str__(self):
        return self.name
