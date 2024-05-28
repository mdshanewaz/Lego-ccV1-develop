# Generated by Django 3.2.16 on 2023-05-05 22:19

from django.db import migrations, models
import guestactions.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=100)),
                ('l_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=500)),
                ('msg', models.TextField(max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='timestamp of creation')),
            ],
            options={
                'verbose_name_plural': 'Contact Us',
            },
        ),
        migrations.CreateModel(
            name='GuestResumeFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file1', models.FileField(upload_to=guestactions.models.guest_resume_location)),
                ('email', models.EmailField(default=None, max_length=200)),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Resume Files by Guest',
                'verbose_name_plural': 'Resume Files by Guest',
            },
        ),
        migrations.CreateModel(
            name='InviteFriends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_first_name', models.CharField(max_length=100)),
                ('guest_last_name', models.CharField(max_length=100)),
                ('guest_email_address', models.CharField(max_length=100)),
                ('friend_first_name', models.CharField(max_length=100)),
                ('friend_email_address', models.CharField(max_length=100)),
                ('consent', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='timestamp of creation')),
                ('updated', models.DateTimeField(auto_now=True, help_text='timestamp of last update')),
            ],
            options={
                'verbose_name_plural': 'Invite Friend List',
            },
        ),
        migrations.CreateModel(
            name='mfeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email_address', models.CharField(max_length=1000)),
                ('product_liked', models.CharField(choices=[('mprod_exp180', 'Exp180'), ('mprod_intprep', 'Dialogue'), ('mprod_proflevel', 'Staircase'), ('mprod_proglang', 'Dialect'), ('mprod_rolebased', 'Identity'), ('mprod_strategy', 'Strategy'), ('mprod_visabased', 'Bandwidth'), ('mprod_xyz', 'General'), ('mprod_adhoc', 'Adhoc'), ('mprod_referral', 'Referral')], default='mprod_exp180', max_length=24)),
                ('feedback', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, help_text='timestamp of creation')),
                ('updated', models.DateTimeField(auto_now=True, help_text='timestamp of last update')),
            ],
            options={
                'verbose_name_plural': 'Feedback',
            },
        ),
        migrations.CreateModel(
            name='SiteSurveyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_used', models.CharField(blank=True, max_length=100, null=True)),
                ('hmpg_design', models.CharField(blank=True, max_length=100, null=True)),
                ('userfriendly', models.CharField(blank=True, max_length=100, null=True)),
                ('promo_offers', models.CharField(blank=True, max_length=100, null=True)),
                ('service_lineup', models.CharField(blank=True, max_length=100, null=True)),
                ('overall_exp', models.CharField(blank=True, max_length=100, null=True)),
                ('recommend', models.CharField(blank=True, max_length=100, null=True)),
                ('message', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='timestamp of creation site survey')),
            ],
        ),
    ]