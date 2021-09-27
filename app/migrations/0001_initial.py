# Generated by Django 3.2.7 on 2021-09-26 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CardDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_last_digit', models.CharField(max_length=6)),
                ('cardholder_name', models.CharField(max_length=50)),
                ('expiry_month', models.CharField(max_length=2)),
                ('expiry_year', models.CharField(max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'card_information',
            },
        ),
        migrations.AddIndex(
            model_name='carddetails',
            index=models.Index(fields=['cardholder_name'], name='card_inform_cardhol_0a633e_idx'),
        ),
    ]
