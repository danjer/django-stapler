from django.forms import ModelForm
from stapler.tests.test_app.models import Bike, Manufacturer
from stapler.forms import StaplerForm

#######################
# FORMS FOR TESTING
#######################


class BikeModelForm(ModelForm):

    class Meta:
        model = Bike
        fields = ['name', 'price']


class ManufacturerModelForm(ModelForm):

    class Meta:
        model = Manufacturer
        fields = ['name', 'revenue']

class BikeManufacturerForm(StaplerForm):

    class Meta:
        modelforms = (BikeModelForm, ManufacturerModelForm)