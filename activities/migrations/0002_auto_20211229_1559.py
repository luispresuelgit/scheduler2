# Generated by Django 3.2.10 on 2021-12-29 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='modified',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='modified',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='survey',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='modified',
        ),
        migrations.AlterField(
            model_name='activity',
            name='schedule',
            field=models.DateTimeField(auto_now=True, verbose_name='schedule'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='active', max_length=35),
        ),
        migrations.AlterField(
            model_name='property',
            name='status',
            field=models.CharField(choices=[('enabled', 'enabled'), ('disabled', 'disabled')], default='enabled', max_length=35),
        ),
        migrations.AlterField(
            model_name='survey',
            name='activity',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, serialize=False, to='activities.activity'),
        ),
    ]
