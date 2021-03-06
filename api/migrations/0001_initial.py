# Generated by Django 2.1.4 on 2018-12-20 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MathematicalObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latex', models.CharField(max_length=65535)),
                ('type', models.CharField(choices=[('S', 'SERIES'), ('P', 'PRODUCT'), ('K', 'FRACTION')], max_length=1)),
                ('convergence_radius', models.CharField(blank=True, max_length=255)),
                ('description', models.FileField(blank=True, upload_to='mathematical_objects/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('functions', models.ManyToManyField(to='api.Function')),
            ],
        ),
        migrations.CreateModel(
            name='Modification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now=True)),
                ('new_description', models.FileField(upload_to='modifications/')),
                ('mathematical_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.MathematicalObject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Proposition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=65535)),
                ('date_created', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='mathematicalobject',
            name='names',
            field=models.ManyToManyField(to='api.Name'),
        ),
        migrations.AddField(
            model_name='mathematicalobject',
            name='related',
            field=models.ManyToManyField(related_name='_mathematicalobject_related_+', to='api.MathematicalObject'),
        ),
        migrations.AddField(
            model_name='mathematicalobject',
            name='tags',
            field=models.ManyToManyField(to='api.Tag'),
        ),
    ]
