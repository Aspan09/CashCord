# Generated by Django 5.0.4 on 2024-04-13 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_remove_bank_card_name_remove_bank_card_name_second_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_card_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cards.cards', verbose_name='Название карты'),
        ),
    ]
