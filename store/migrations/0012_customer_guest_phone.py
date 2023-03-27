# Generated by Django 4.1.7 on 2023-03-27 10:26

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0011_customer_guest_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="guest_phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, null=True, region="UA"
            ),
        ),
    ]
