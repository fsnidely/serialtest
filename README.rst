README
======


This is a sandbox for testing a serialization problem when including
natural keys with a One-To-One linked table.

The problem occurs when serializing with use_natural_primary_keys=True,
and use_natural_foreign_keys=True. The parent_link field is not included
in the 'fields' structure in the json format (fails similarly for xml as
well).

    Equivalent to this unanswered stackoverflow:
    https://stackoverflow.com/questions/28702215/natural-key-serialize-django-model-with-one-to-one-field-as-primary-key

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

    - Product2: Simple inheiritance with implied PK of 'thing_ptr'
    - Product3: Inheiritance with a OneToOneField and parent_link=True
    - Product4: Non-inherited instance with a OneToOneField and primary_key=True

        (Product4 was my original variation.)


Example:
~~~~~~~~

The following examples show the omitted natural key for Product3, whereas
Product has been altered to ALWAYS serialize 'thing' (parent_link to Thing).

Product3 has no primary key available (whether a PK or a NK) for the instances
that use_natural_primary_keys=True.

::

    2116$ pyman shell
    Python 3.6.5 (default, Mar 29 2018, 03:28:50) 
    [GCC 5.4.0 20160609] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
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

    >>> 


Environment:
~~~~~~~~~~~~

- Python 3.6.5
- Django==2.0.6
- pylint-django==0.11.1
- Pillow==5.1.0
