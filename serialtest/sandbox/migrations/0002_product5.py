# Generated by Django 2.0.6 on 2018-06-05 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sandbox', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product5',
            fields=[
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='sandbox.Thing')),
                ('prod_secs', models.IntegerField(verbose_name='Production seconds')),
                ('low_level', models.IntegerField(default=-1, verbose_name='Low-level code')),
            ],
        ),
    ]