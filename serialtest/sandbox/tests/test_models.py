"""Sandbox: Models unit tests"""

from django.core import serializers
from django.db import models
from django.test import TestCase

from sandbox.models import Kind, Materiel, Product, Thing


class ModelNaturalKeyTestMixin():
    """Test natural_key() and get_by_natural_key() methods.

    Requires:

        self.model: Model being tested.

        self.obj: Instance of Model being tested

        self.obj_nk: Expected natural_key() of instance being tested.
    """
    def test_validate_naturalkeymixin(self):
        """Validate that ModelNaturalKeyTestMixin has required attributes."""
        self.assertTrue(issubclass(self.model, models.Model))
        self.assertIsInstance(self.obj, self.model)
        self.assertIsNotNone(self.obj_nk)

    def test_natural_key(self):
        """Test obj.natural_key() comparing to obj_nk"""
        self.assertEqual(
            self.obj_nk, self.obj.natural_key(),
            f'\nObject:\n\t{type(self.obj)}:'
            f' [{self.obj.pk}]{repr_from_model(self.obj)}'
        )


    def test_get_by_natural_key(self):
        """Test model.objects.get_by_natural_key(*obj_nk) returns obj"""
        getobj = self.model.objects.get_by_natural_key(*self.obj_nk)
        self.assertEqual(self.obj, getobj)


def repr_from_model(instance, use_local=True):
    """Return a string representing the fields of the model."""
    buf = []
    error = None
    fields = (
        instance._meta.local_concrete_fields if use_local
        else instance._meta.get_fields())
    for field in fields:  # local_concrete_fields or get_fields()
        try:
            buf.append(f'"{field.name}": "{getattr(instance, field.name, None)}"')
        except AttributeError as exc:
            buf.append(f'"{field.name}": "<{exc}>"')
            error = AttributeError
    bufout = ', '.join(buf)
    out = f'<{instance.__class__.__name__}({bufout})>'
    if error:
        raise error(out)
    return out


class ModelSerializerTestMixin():
    """Test serializing/deserializing a model.

    Requires:

        self.obj: Instance of Model being tested
    """

    def test_json_serializer(self):
        """Test serialization/deserialization using JSON format."""
        data = serializers.serialize("json", [self.obj], indent=4)

        # deserialize and compare to original
        desobj = list(serializers.deserialize("json", data))[0]

        self.assertEqual(
            self.obj, desobj.object,
            f'\nObject:\n\t{type(self.obj)}: {repr_from_model(self.obj)}'
            f'\nSerialized to:\n\t{type(desobj.object)}: {repr_from_model(desobj.object)}'
            f'\nSerialization:\n{data}')

    def test_json_natural_key(self):
        """Test serialization/deserialization using JSON format and using natural_key()."""
        data = serializers.serialize(
            "json", [self.obj], indent=4,
            use_natural_primary_keys=True, use_natural_foreign_keys=True)

        # deserialize and compare to original
        try:
            desobj = list(serializers.deserialize("json", data))[0]
        except serializers.base.DeserializationError as exc:
            raise ValueError(
                f'\nObject:\n\t{type(self.obj)}: {repr_from_model(self.obj)}'
                f'\nSerialization:\n{data}'
            ) from exc

        self.assertEqual(
            self.obj, desobj.object,
            f'\nObject:\n\t{type(self.obj)}: {repr_from_model(self.obj)}'
            f'\nSerialized to:\n\t{type(desobj.object)}: {repr_from_model(desobj.object)}'
            f'\nSerialization:\n{data}')


class ModelTestCollectionMixins(ModelNaturalKeyTestMixin, ModelSerializerTestMixin):
    """A collection of Model test mixins:

    * ModelNaturalKeyTestMixin

    * ModelSerializerTestMixin
    """
    pass


class KindModelTest(TestCase, ModelTestCollectionMixins):
    """Test the Kind model with the ModelTestCollectionMixins.
    """
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.model = Kind

        cls.obj = Kind(
            iden='F', name='Fruit', desc='You know ... fruit', rank=1)
        cls.obj.save()
        cls.obj_pk = cls.obj.pk

        cls.obj_nk = (cls.obj.iden,)


class ThingModelTest(TestCase, ModelTestCollectionMixins):
    """Test the Thing model with the ModelTestCollectionMixins.
    """
    def setUp(self):
        self.model = Thing

        self.kind = Kind(
            iden='F', name='Fruit', desc='You know ... fruit', rank=1)
        self.kind.save()

        self.obj = Thing(
            iden='F-A', kind=self.kind, name='Apple',
            desc='You know ... apple', rank=1)
        self.obj.save()
        self.obj_pk = self.obj.pk

        self.obj_nk = (self.obj.iden,)


class ProductModelTest(TestCase, ModelTestCollectionMixins):
    """Test the Product model with the ModelTestCollectionMixins.
    """
    def setUp(self):
        self.model = Product

        # Tweak the 'thing' field's 'serialize' attribute.
        # This overrides the normally 'False' value, which omits
        # the 'thing' field from serialization when using
        # the natural_key().
        #
        # True: Succeeds, False: Fails
        self.model._meta.get_field('thing').serialize = True

        self.kind = Kind(
            iden='F', name='Fruit', desc='You know ... fruit', rank=1)
        self.kind.save()

        self.thing = Thing(
            iden='F-A', kind=self.kind, name='Apple',
            desc='You know ... apple', rank=1)
        self.thing.save()

        self.obj = Product(thing=self.thing, prod_secs=42)
        # self.obj.thing = self.thing
        self.obj.save_base(raw=True)

        # refresh after saving
        self.obj.refresh_from_db()

        self.obj_pk = self.obj.pk
        self.assertEqual(self.obj_pk, self.thing.pk)

        # Natural key is inherited from Thing
        self.obj_nk = self.thing.natural_key()


class ProductModelFailTest(ProductModelTest):
    """Failing Test of the Product model with the ModelTestCollectionMixins.

    Configure the Product Model to fail the serialization test!
    """
    def setUp(self):
        super().setUp()

        # Tweak the 'thing' field's 'serialize' attribute.
        # This overrides the normally 'False' value, which omits
        # the 'thing' field from serialization when using
        # the natural_key().
        #
        # True: Succeeds, False: Fails
        self.model._meta.get_field('thing').serialize = False


class MaterielModelTest(TestCase, ModelTestCollectionMixins):
    """Test the Materiel model with the ModelTestCollectionMixins.
    """
    def setUp(self):
        self.model = Materiel

        self.kind = Kind(
            iden='F', name='Fruit', desc='You know ... fruit', rank=1)
        self.kind.save()

        self.kind2 = Kind(
            iden='B', name='Baked', desc='Something baked.', rank=2)
        self.kind2.save()

        self.thing = Thing(
            iden='F-A', kind=self.kind, name='Apple',
            desc='You know ... apple', rank=1)
        self.thing.save()

        self.thing2 = Thing(
            iden='F-P', kind=self.kind2, name='Apple Pie',
            desc='A Pie made with apples', rank=2)
        self.thing2.save()

        self.prod = Product(thing=self.thing, prod_secs=42)
        self.prod.save_base(raw=True)
        # refresh after saving
        self.prod.refresh_from_db()

        self.prod2 = Product(thing=self.thing2, prod_secs=360)
        self.prod2.save_base(raw=True)
        # refresh after saving
        self.prod2.refresh_from_db()

        self.obj = Materiel(
            parent=self.prod2, component=self.prod, quantity=6)
        self.obj.save()
        self.obj_pk = self.obj.pk

        self.obj_nk = self.prod2.natural_key() + self.prod.natural_key()
