"""Database models for Sandbox App"""

import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.html import format_html

STATIC_IMAGES_PATH = 'sandbox/images'
IMAGE_ASSET_STORAGE = FileSystemStorage(
    location=os.path.join(settings.STATIC_ROOT, STATIC_IMAGES_PATH),
    base_url=os.path.join(settings.STATIC_URL, STATIC_IMAGES_PATH))


class KindManager(models.Manager):
    def get_by_natural_key(self, iden):
        return self.get(iden=iden)


class Kind(models.Model):
    """Kind Model is the Kind of thing like Expansion item or Store item"""
    objects = KindManager()

    iden = models.CharField('Kind', max_length=8, unique=True)
    name = models.CharField('Name', max_length=80)
    desc = models.CharField('Description', max_length=255, blank=True)
    rank = models.IntegerField('Rank', default=0)

    class Meta:
        ordering = ('rank', 'id',)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.iden,)


class ThingManager(models.Manager):
    def get_by_natural_key(self, iden):
        return self.get(iden=iden)


class Thing(models.Model):
    """General collection of objects.

    Named 'things' instead of objects as that would get confusing referring to Object.objects, etc.
    """
    objects = ThingManager()

    iden = models.CharField('Thing', max_length=8, unique=True)
    kind = models.ForeignKey(Kind, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=80)
    desc = models.CharField('Description', max_length=255)
    rank = models.IntegerField('Rank', default=0)
    image = models.ImageField('Thing', storage=IMAGE_ASSET_STORAGE, blank=True)

    class Meta:
        ordering = ('kind__rank', 'rank', 'id',)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.iden,)

    def img_html(self):
        """Image tag for image file."""
        return format_html(
            '<img src="{0}" alt="{1}" title={1}>',
            self.image.url,
            self.name)
    img_html.short_description = 'Thing'

    def img_name_html(self):
        """Image tag for image file."""
        return format_html(
            '{0} {1}',
            self.img_html(),
            self.name)
    img_name_html.short_description = 'Thing'


class Product(Thing):
    """Product for things that can be produced.

    A child record of Thing.
    """
    thing = models.OneToOneField(
        Thing, on_delete=models.CASCADE, parent_link=True)
    prod_secs = models.IntegerField('Production seconds')
    low_level = models.IntegerField('Low-level code', default=-1)
# Tweak the 'thing' field's 'serialize' attribute.
# This overrides the normally 'False' value, which omits
# the 'thing' field from serialization when using
# the natural_key().
Product._meta.get_field('thing').serialize = True


class MaterielManager(models.Manager):
    def get_by_natural_key(self, parent, component):
        return self.get(
            parent__thing__iden=parent, component__thing__iden=component)


class Materiel(models.Model):
    """Materiel Bill-Of-Material records."""
    objects = MaterielManager()

    parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='materiels')
    component = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='usedin')
    quantity = models.IntegerField()

    class Meta:
        unique_together = (('parent', 'component'),)

    def natural_key(self):
        return self.parent.natural_key() + self.component.natural_key()
    natural_key.dependencies = ['sandbox.product']

    def clean(self):
        """Validate BOM relationship."""
        if self.parent and self.component and self.parent == self.component:
            raise ValidationError('Parent and component can not be the same.')

    def parent_name(self):
        return self.parent.thing.name

    def component_name(self):
        return self.component.thing.name

    def __str__(self):
        return f'{self.parent_name()} :-- {self.quantity} * {self.component_name()}'


class Product2(Thing):
    """Experimental Product model extending Thing model."""
    prod_secs = models.IntegerField('Production seconds')
    low_level = models.IntegerField('Low-level code', default=-1)
# # Tweak the 'thing' field's 'serialize' attribute.
# Product2._meta.get_field('thing_ptr').serialize = True


class Product3(Thing):
    """Experimental Product model extending Thing model."""
    thing = models.OneToOneField(
        Thing, on_delete=models.CASCADE, parent_link=True)
    prod_secs = models.IntegerField('Production seconds')
    low_level = models.IntegerField('Low-level code', default=-1)
# # Tweak the 'thing' field's 'serialize' attribute.
# Product3._meta.get_field('thing').serialize = True


class Product4Manager(models.Manager):
    """Old Product model manager."""
    def get_by_natural_key(self, iden):
        return self.get(thing__iden=iden)


class Product4(models.Model):
    """Old Product model."""
    objects = Product4Manager()

    thing = models.OneToOneField(
        Thing, on_delete=models.CASCADE, primary_key=True)
    prod_secs = models.IntegerField('Production seconds')
    low_level = models.IntegerField('Low-level code', default=-1)

    class Meta:
        ordering = ('thing__kind__rank', 'thing__rank')

    def __str__(self):
        return self.thing.name

    def natural_key(self):
        return self.thing.natural_key()
    natural_key.dependencies = ['sandbox.thing']
# Tweak the 'thing' field's 'serialize' attribute.
# This overrides the normally 'False' value, which omits
# the 'thing' field from serialization when using
# the natural_key().
Product4._meta.get_field('thing').serialize = True
