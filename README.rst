README
======

FIXED: Release of Django 2.1 has fixed this problem!

Update: The `Ticket #29472 <https://code.djangoproject.com/ticket/29472>`_
was marked a duplicate of 
`#24607: Bug: Serialization (and deserialization) of MTI models doesn't work with ... (closed: fixed)
<https://code.djangoproject.com/ticket/24607>`_.

This is a sandbox for testing a serialization problem when including
natural keys with a One-To-One linked table.

The problem occurs when serializing with use_natural_primary_keys=True,
and use_natural_foreign_keys=True. The parent_link field is not included
in the 'fields' structure in the json format (fails similarly for xml as
well).

    Equivalent to this unanswered stackoverflow:
    https://stackoverflow.com/questions/28702215/natural-key-serialize-django-model-with-one-to-one-field-as-primary-key

Django Bug report: `Ticket #29472
"Natural key not serializing for primary_key OneToOneField"
<https://code.djangoproject.com/ticket/29472>`_.

A work-around that will include the omitted parent_link field is to alter
the 'serialize' attribute of the OneToOneField to True. This will always
include the parent_link field even when the natural keys are not specified.
However, deserialization works in either case, so it appears to be benign.

An example of this is the Product model which is NOT including the natural key,
unless the 'serialize' attribute of 'thing' is set to true.

The sandbox.tests.test_models.ProductModelTest alters the Product model
to PASS the serialization test.

The sandbox.tests.test_models.ProductModelFailTest alters the Product model
to FAIL the serialization test.

The Product model in models.py already has the alteration to succeed. The test cases
ensure the value is set as expected.

Some alternate variations (which do not alter the serialize attribute of the
respective PK's):

    - Product2: Simple inheritance with implied PK of 'thing_ptr'
    - Product3: Inheritance with a OneToOneField and parent_link=True
    - Product4: Non-inherited instance with a OneToOneField and primary_key=True

        (Product4 was my original variation.)
    - Product5: Non-inherited instance with a ForeignKey and primary_key=True

        Notice that a ForeignKey used as the primary key also fails to serialize
        the natural key. Of course, there is a warning that the OneToOneField is
        better suited for the primary key. Nevertheless, it is treated like the
        OneToOneField when serializing natural keys.


Example:
~~~~~~~~

The following examples show the omitted natural key for Product3, whereas
Product has been altered to ALWAYS serialize 'thing' (parent_link to Thing).

Product3 has no primary key available (whether a PK or a NK) for the instances
that use_natural_primary_keys=True. Except when use_natural_primary_keys=False
and use_natural_foreign_keys=True, where it has an integer PK, but no NK.


>>> from django.core import serializers
>>> from sandbox.models import Kind, Thing, Product, Product3
>>> kind = Kind(iden='F', name='Fruit', desc='You know ... fruit', rank=1)
>>> kind.save()
>>> thing = Thing(iden='F-A', kind=kind, name='Apple', desc='You know ... apple', rank=1)
>>> thing.save()
>>> prod = Product(thing=thing, prod_secs=42)
>>> prod.save_base(raw=True)
>>> prod.refresh_from_db()
>>> prod3 = Product3(thing=thing, prod_secs=42)
>>> prod3.save_base(raw=True)
>>> prod3.refresh_from_db()
>>> print(serializers.serialize("json", [prod, prod3], indent=4, use_natural_primary_keys=True, use_natural_foreign_keys=True))
[
{
    "model": "sandbox.product",
    "fields": {
        "thing": [
            "F-A"
        ],
        "prod_secs": 42,
        "low_level": -1
    }
},
{
    "model": "sandbox.product3",
    "fields": {
        "prod_secs": 42,
        "low_level": -1
    }
}
]

>>> print(serializers.serialize("json", [prod, prod3], indent=4, use_natural_primary_keys=True))
[
{
    "model": "sandbox.product",
    "fields": {
        "thing": 2,
        "prod_secs": 42,
        "low_level": -1
    }
},
{
    "model": "sandbox.product3",
    "fields": {
        "prod_secs": 42,
        "low_level": -1
    }
}
]

>>> print(serializers.serialize("json", [prod, prod3], indent=4, use_natural_foreign_keys=True))
[
{
    "model": "sandbox.product",
    "pk": 2,
    "fields": {
        "thing": [
            "F-A"
        ],
        "prod_secs": 42,
        "low_level": -1
    }
},
{
    "model": "sandbox.product3",
    "pk": 2,
    "fields": {
        "prod_secs": 42,
        "low_level": -1
    }
}
]

>>> print(serializers.serialize("json", [prod, prod3], indent=4))
[
{
    "model": "sandbox.product",
    "pk": 2,
    "fields": {
        "thing": 2,
        "prod_secs": 42,
        "low_level": -1
    }
},
{
    "model": "sandbox.product3",
    "pk": 2,
    "fields": {
        "prod_secs": 42,
        "low_level": -1
    }
}
]


Environment:
~~~~~~~~~~~~

- Python 3.6.5
- Django==2.0.6
- pylint-django==0.11.1
- Pillow==5.1.0


Credit:
~~~~~~~

`MIT License <LICENSE.txt>`_

Copyright (c) 2018 Ferd Snidely
