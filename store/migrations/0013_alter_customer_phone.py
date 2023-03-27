# Generated by Django 4.1.7 on 2023-03-27 11:00

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0012_customer_guest_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, null=True, region="UA", unique=True
            ),
        ),
    ]