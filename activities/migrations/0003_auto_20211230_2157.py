# Generated by Django 3.2.10 on 2021-12-31 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20211229_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='schedule',
            field=models.DateTimeField(verbose_name='schedule'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('cancelled', 'cancelled'), ('done', 'done')], default='active', max_length=35),
        ),
    ]
