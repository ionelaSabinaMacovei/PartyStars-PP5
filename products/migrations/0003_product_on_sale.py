# Generated by Django 3.2.21 on 2023-09-14 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20230908_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='on_sale',
            field=models.BooleanField(default=False),
        ),
    ]
