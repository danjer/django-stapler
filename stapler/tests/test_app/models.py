from django.db import models

#########################
# MODELS USED FOR TESTING
########################

class Country(models.Model):
    name = models.CharField(max_length=100)


class Wheel(models.Model):
    brand = models.CharField(max_length=100)
    available_countries = models.ManyToManyField(Country, 'available_wheels', blank=True)


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    revenue = models.CharField(max_length=100)
    country = models.ForeignKey('Country', null=True, blank=True, on_delete=models.SET_NULL)


class Bike(models.Model):
    name = models.CharField(max_length=100)
    frame_type = models.CharField(max_length=100, default='roadbike')
    price = models.IntegerField()
    available_countries = models.ManyToManyField(Country, 'available_bikes')