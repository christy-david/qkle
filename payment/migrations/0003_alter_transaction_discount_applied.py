# Generated by Django 4.2.7 on 2024-01-03 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_rename_amount_transaction_base_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='discount_applied',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
