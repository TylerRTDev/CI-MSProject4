# Generated by Django 4.2.7 on 2025-06-24 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_alter_checkoutorder_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkoutorder',
            name='order_number',
            field=models.CharField(blank=True, max_length=5, null=True, unique=True),
        ),
    ]
