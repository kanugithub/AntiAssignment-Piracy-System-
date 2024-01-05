# Generated by Django 4.2.6 on 2023-10-14 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('checkassignment', '0002_delete_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=100)),
                ('student_roll_no', models.CharField(max_length=15, unique=True)),
                ('student_password', models.CharField(max_length=128)),
            ],
        ),
    ]
