# Generated by Django 4.1.5 on 2023-03-02 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('np_app', '0004_rename_client_name_appointment_user_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Appointment',
        ),
        migrations.RemoveField(
            model_name='category',
            name='subscribers',
        ),
        migrations.DeleteModel(
            name='SubscribersUser',
        ),
    ]