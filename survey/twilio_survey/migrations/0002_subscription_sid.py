# Generated by Django 3.1.6 on 2021-02-07 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twilio_survey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='sid',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
