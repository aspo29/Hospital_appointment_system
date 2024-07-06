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

