from django import forms
from stapler.tests.test_app.models import Bike, Manufacturer, Wheel
from stapler.forms import StaplerForm

#######################
# FORMS FOR TESTING
#######################


class BikeModelForm(forms.ModelForm):

    class Meta:
        model = Bike
        fields = ['name', 'price']

class BikeModelForm2(forms.ModelForm):

    class Meta:
        model = Bike
        fields = ['name', 'price', 'available_countries']

class WheelModelForm(forms.ModelForm):

    class Meta:
        model = Wheel
        fields = ['brand', 'available_countries']

class ManufacturerModelForm(forms.ModelForm):

    class Meta:
        model = Manufacturer
        fields = ['name', 'revenue']

class BikeManufacturerForm(StaplerForm):

    class Meta:
        modelforms = (BikeModelForm, ManufacturerModelForm)


class CustomBikeManufacturerForm(StaplerForm):

    bike__name = forms.IntegerField()

    class Meta:
        modelforms = (BikeModelForm, ManufacturerModelForm)


class BikeWheelForm(StaplerForm):

    class Meta:
        modelforms = (BikeModelForm, WheelModelForm)
        auto_prefix = False

class M2mBikeManufacturerForm(StaplerForm):

    class Meta:
        modelforms = (BikeModelForm2, ManufacturerModelForm)

