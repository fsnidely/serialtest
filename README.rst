README
======


This is a sandbox for testing a serialization problem with a One-To-One linked table.

The problem occurs when serializing with use_natural_primary_keys=True,
and use_natural_foreign_keys=True. The parent_link field is not included in the 'fields'
structure in the json format (fails similarly for xml as well).

A work-around that will include the omitted parent_link field is to set the 'serialize'
attribute to True. This will always include the parent_link field even when the natural
keys are not specified. However, deserialization works in either case, so it appears to
be benign.

The Product model is NOT including the natural_key()!

    Equivalent to this unanswered stackoverflow:
    https://stackoverflow.com/questions/28702215/natural-key-serialize-django-model-with-one-to-one-field-as-primary-key

The sandbox.tests.test_models.ProductModelTest patches the Product model
to PASS the serialization test.

The sandbox.tests.test_models.ProductModelFailTest patches the Product model
to FAIL the serialization test.

The Product model in models.py already has the patch set to succeed. The test cases
ensure the value is set as expected.


Environment:
~~~~~~~~~~~~

- Python 3.6.5
- Django==2.0.6
- pylint-django==0.11.1
- Pillow==5.1.0
