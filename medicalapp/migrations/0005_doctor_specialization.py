# Generated by Django 4.2.7 on 2024-02-18 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicalapp', '0004_remove_medicine_qty_remove_prescription_prescdate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='specialization',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
