from django.test import TestCase
from .test_app.models import Bike, Manufacturer, Country, Wheel
from stapler.tests.test_app.forms import BikeManufacturerForm, CustomBikeManufacturerForm, M2mBikeManufacturerForm, \
    BikeWheelForm, BikeModelForm
from django import forms

# Create your tests here.
class StaplerFormTestCase(TestCase):

    def test_copies_fields_with_clashing_names(self):
        form = BikeManufacturerForm()
        self.assertEqual(4, len(form.fields))

    def test_handles_auto_prefix_option(self):
        form = BikeWheelForm()
        field_names = set([fn for fn in form.fields.keys()])
        expected_field_names = set(('price', 'brand', 'name', 'available_countries'))
        self.assertEqual(field_names, expected_field_names)


    def test_does_not_override_declared_fields(self):
        form = CustomBikeManufacturerForm()
        self.assertEqual(4, len(form.fields))
        self.assertEqual(type(form.fields['bike__name']), forms.IntegerField)

    def test_accepts_instance_keyword(self):
        bike = Bike.objects.create(name='Propel', price=200)
        form = BikeManufacturerForm(instance=bike)
        self.assertEqual(form.bike_instance, bike)

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

    def tests_valid_with_auto_prefix_off(self):
        data = {'brand': 'Giant', 'name': 'Propel', 'price': 300}
        form = BikeWheelForm(data)
        self.assertTrue(form.is_valid())


    def test_returns_saved_models(self):
        form = BikeManufacturerForm({'bike__name': 'Propel', 'manufacturer__name': 'Giant',
                                          'manufacturer__revenue': '30000,-', 'bike__price': 300})
        form.is_valid()
        result = form.save()
        b = Bike.objects.first()
        m = Manufacturer.objects.first()
        self.assertEqual(b, result['bike_instance'])
        self.assertEqual(m, result['manufacturer_instance'])

    def test_returns_saved_models_with_auto_prefix_off(self):
        data = {'brand': 'Giant', 'name': 'Propel', 'price': 300}
        form = BikeWheelForm(data)
        result = form.save()
        bike = result['bike_instance']
        wheel = result['wheel_instance']
        self.assertEqual(wheel.brand, 'Giant')
        self.assertEqual(bike.price, 300)
        self.assertEqual(bike.pk, 1)
        self.assertEqual(wheel.pk, 1)



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

    def test_saves_m2m(self):
        countries = [Country.objects.create(name=f'country_{0}') for i in range(3)]
        for c in countries:
            c.save()

        data = {'bike__name': 'Oltre xr4',
                'bike__price': 300,
                'bike__available_countries': [1,2,3],
                'manufacturer__name': 'Bianchi',
                'manufacturer__revenue': '30000,-'}
        form = M2mBikeManufacturerForm(data)
        result = form.save(commit=True)
        bike = result['bike_instance']
        self.assertTrue(len(bike.available_countries.all()), 3)

    def test_saves_m2m_with_auto_prefix_off(self):
        countries = [Country.objects.create(name=f'country_{0}') for i in range(3)]
        for c in countries:
            c.save()

        data = {'brand': 'Giant', 'name': 'Propel', 'price': 300, 'available_countries': [1, 2, 3]}
        form = BikeWheelForm(data)
        result = form.save()
        bike = result['bike_instance']
        wheel = result['wheel_instance']
        self.assertEqual(wheel.brand, 'Giant')
        self.assertEqual(bike.price, 300)
        self.assertEqual(bike.pk, 1)
        self.assertEqual(wheel.pk, 1)
        self.assertEqual(len(wheel.available_countries.all()), 3)

    def test_required_modelforms_option(self):
        for _ in range(2):
            c = Country.objects.create(name=f'land_{_}')
            c.save()

        data = {'name': 'Giant', 'price': 2000, 'available_countries': [1, 2]}
        form = BikeWheelForm(data)
        self.assertTrue(BikeModelForm in form._meta.required)
        self.assertTrue(form.is_valid())

    def test_saves_valid_instances_only(self):
        for _ in range(2):
            c = Country.objects.create(name=f'land_{_}')
            c.save()

        data = {'name': 'Giant', 'price': 2000, 'available_countries': [1, 2]}
        form = BikeWheelForm(data)
        self.assertTrue(BikeModelForm in form._meta.required)
        self.assertTrue(form.is_valid())
        results = form.save()
        saved_bike = results['bike_instance']
        failed_wheel = results['wheel_instance']

        self.assertEqual(len(Bike.objects.all()), 1)
        self.assertEqual(len(Wheel.objects.all()), 0)
        self.assertEqual(saved_bike.pk, 1)
        self.assertEqual(failed_wheel, None)

    # def test_overrides_save_method(self):
    #     raise Exception('TODO')