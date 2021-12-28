# Generated by Django 3.2.10 on 2021-12-28 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('title', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=35)),
                ('schedule', models.DateTimeField(auto_now=True, verbose_name='disabled at')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('title', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=35)),
                ('address', models.TextField(blank=True, verbose_name='text')),
                ('description', models.TextField(blank=True, verbose_name='text')),
                ('disabled_at', models.DateTimeField(null=True, verbose_name='disabled at')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('answers', models.JSONField()),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.activity')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.property'),
        ),
    ]