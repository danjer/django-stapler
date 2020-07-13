from django.test import TestCase
from .test_app.models import Bike, Manufacturer
from stapler.tests.test_app.forms import BikeManufacturerForm

# Create your tests here.
class StaplerFormTestCase(TestCase):

    def test_copies_fields(self):
        form = BikeManufacturerForm()
        self.assertEqual(4, len(form.fields))

    def test_handles_clashing_fields(self):
        pass

    def test_is_not_bound(self):
        bike = Bike.objects.create(name='Propel', price=200)
        manufacturer = Manufacturer.objects.create(name='Giant', revenue='2000.000,-')
        form = BikeManufacturerForm(instances=(bike, manufacturer))
        self.assertFalse(form.is_bound)

    def test_is_bound(self):
        form = BikeManufacturerForm({})
        self.assertTrue(form.is_bound)

    def test_loads_instances_corretly(self):
        bike = Bike.objects.create(name='Propel', price=200)
        manufacturer = Manufacturer.objects.create(name='Giant', revenue='2000.000,-')
        form = BikeManufacturerForm(instances=(bike, manufacturer))
        self.assertEqual(form.manufacturer_instance, manufacturer)
        self.assertEqual(form.bike_instance, bike)

    def test_loads_initial_from_instances(self):
        bike = Bike.objects.create(name='Propel', price=200)
        manufacturer = Manufacturer.objects.create(name='Giant', revenue='2000.000,-')
        form = BikeManufacturerForm(instances=(bike, manufacturer))
        self.assertEqual(form.initial['bike__price'], 200)
        self.assertEqual(form.initial['bike__name'], 'Propel')

    def test_initial_overrides_instance(self):
        bike = Bike.objects.create(name='Propel', price=200)
        form = BikeManufacturerForm(instances=(bike,), initial={'bike__name': 'Oltre xr4'})
        self.assertEqual(form.initial['bike__name'], 'Oltre xr4')

    def test_valid_invalid(self):
        form = BikeManufacturerForm({'bike__name': 'Propel', 'manufacturer__name': 'Giant',
                                          'manufacturer__revenue': '30000,-'})
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_valid_valid(self):
        form = BikeManufacturerForm({'bike__name': 'Propel', 'manufacturer__name':
            'Giant', 'manufacturer__revenue': '30000,-', 'bike__price': 300})
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_saves_models(self):
        form = BikeManufacturerForm({'bike__name': 'Propel', 'manufacturer__name': 'Giant',
                                          'manufacturer__revenue': '30000,-', 'bike__price': 300})
        form.is_valid()
        result = form.save()
        b = Bike.objects.first()
        m = Manufacturer.objects.first()
        self.assertEqual(b.price, 300)
        self.assertEqual(m.name, 'Giant')

    def test_returns_saved_models(self):
        form = BikeManufacturerForm({'bike__name': 'Propel', 'manufacturer__name': 'Giant',
                                          'manufacturer__revenue': '30000,-', 'bike__price': 300})
        form.is_valid()
        result = form.save()
        b = Bike.objects.first()
        m = Manufacturer.objects.first()
        self.assertEqual(b, result['bike_instance'])
        self.assertEqual(m, result['manufacturer_instance'])

    def test_updates_models(self):
        bike = Bike.objects.create(name='Propel', price=200)
        manufacturer = Manufacturer.objects.create(name='Giant', revenue='2000.000,-')
        form = BikeManufacturerForm({'bike__name': 'Oltre xr4', 'manufacturer__name': 'Bianchi',
                                          'manufacturer__revenue': '30000,-', 'bike__price': 300},
                                    instances=(bike, manufacturer))
        form.is_valid()
        form.save()
        b = Bike.objects.first()
        m = Manufacturer.objects.first()
        self.assertEqual(b.price, 300)
        self.assertEqual(b.name, 'Oltre xr4')
        self.assertEqual(m.name, 'Bianchi')
        self.assertEqual(m.revenue, '30000,-')
        self.assertEqual(b.pk, bike.pk)
        self.assertEqual(m.pk, manufacturer.pk)

