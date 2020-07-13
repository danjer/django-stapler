from django import forms
from stapler.tests.test_app.models import Bike, Manufacturer
from stapler.forms import StaplerForm

#######################
# FORMS FOR TESTING
#######################


class BikeModelForm(forms.ModelForm):

    class Meta:
        model = Bike
        fields = ['name', 'price']


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