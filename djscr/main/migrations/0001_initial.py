# Generated by Django 4.2.5 on 2023-09-29 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vuz', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('publication_count', models.CharField(max_length=10)),
                ('hirsh', models.CharField(max_length=10)),
                ('vac', models.CharField(max_length=10)),
            ],
        ),
    ]
