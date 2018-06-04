# Generated by Django 2.0.6 on 2018-06-04 01:14

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iden', models.CharField(max_length=8, unique=True, verbose_name='Kind')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('desc', models.CharField(blank=True, max_length=255, verbose_name='Description')),
                ('rank', models.IntegerField(default=0, verbose_name='Rank')),
            ],
            options={
                'ordering': ('rank', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Materiel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iden', models.CharField(max_length=8, unique=True, verbose_name='Thing')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('desc', models.CharField(max_length=255, verbose_name='Description')),
                ('rank', models.IntegerField(default=0, verbose_name='Rank')),
                ('image', models.ImageField(blank=True, storage=django.core.files.storage.FileSystemStorage(base_url='/static/sandbox/images', location='/home/frank/prj/python/serialtest/static/sandbox/images'), upload_to='', verbose_name='Thing')),
            ],
            options={
                'ordering': ('kind__rank', 'rank', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('thing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, to='sandbox.Thing')),
                ('prod_secs', models.IntegerField(verbose_name='Production seconds')),
                ('low_level', models.IntegerField(default=-1, verbose_name='Low-level code')),
            ],
            bases=('sandbox.thing',),
        ),
        migrations.CreateModel(
            name='Product2',
            fields=[
                ('thing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sandbox.Thing')),
                ('prod_secs', models.IntegerField(verbose_name='Production seconds')),
                ('low_level', models.IntegerField(default=-1, verbose_name='Low-level code')),
            ],
            bases=('sandbox.thing',),
        ),
        migrations.CreateModel(
            name='Product3',
            fields=[
                ('thing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sandbox.Thing')),
                ('prod_secs', models.IntegerField(verbose_name='Production seconds')),
                ('low_level', models.IntegerField(default=-1, verbose_name='Low-level code')),
            ],
            bases=('sandbox.thing',),
        ),
        migrations.CreateModel(
            name='Product4',
            fields=[
                ('thing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, to='sandbox.Thing')),
                ('prod_secs', models.IntegerField(verbose_name='Production seconds')),
                ('low_level', models.IntegerField(default=-1, verbose_name='Low-level code')),
            ],
            options={
                'ordering': ('thing__kind__rank', 'thing__rank'),
            },
        ),
        migrations.AddField(
            model_name='thing',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sandbox.Kind'),
        ),
        migrations.AddField(
            model_name='materiel',
            name='component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usedin', to='sandbox.Product'),
        ),
        migrations.AddField(
            model_name='materiel',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materiels', to='sandbox.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='materiel',
            unique_together={('parent', 'component')},
        ),
    ]
