# Generated by Django 5.1.2 on 2024-12-13 15:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('food', '0001_initial'),
        ('payment', '0002_alter_payment_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(related_name='orders', to='food.food')),
                ('payment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='payment.payment')),
            ],
        ),
    ]
