# Generated by Django 4.2 on 2023-05-02 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-price', 'name')},
        ),
    ]