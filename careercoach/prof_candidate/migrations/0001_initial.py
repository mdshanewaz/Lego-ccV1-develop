# Generated by Django 3.2.16 on 2023-05-01 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resumeweb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DispCause',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(default='Late Delivery', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrderCancellationRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=2000)),
                ('created_for', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='timestamp of creation order cancellation request')),
                ('submitted_by', models.EmailField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceFeedbackModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='timestamp of creation order feedback')),
                ('submited_by', models.EmailField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ResumeFormType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique ID', primary_key=True, serialize=False)),
                ('Exp_1', models.CharField(default='Exp_1', max_length=500)),
                ('start_date_1', models.DateField(blank=True, null=True)),
                ('end_date_1', models.DateField(blank=True, null=True)),
                ('Job_Duties_1', models.TextField(blank=True, max_length=7000, null=True)),
                ('Exp_2', models.CharField(default='Exp_2', max_length=500)),
                ('start_date_2', models.DateField(blank=True, null=True)),
                ('end_date_2', models.DateField(blank=True, null=True)),
                ('Job_Duties_2', models.TextField(blank=True, max_length=7000, null=True)),
                ('Exp_3', models.CharField(default='Exp_3', max_length=500)),
                ('start_date_3', models.DateField(blank=True, null=True)),
                ('end_date_3', models.DateField(blank=True, null=True)),
                ('Job_Duties_3', models.TextField(blank=True, max_length=7000, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='timestamp of creation')),
                ('updated', models.DateTimeField(auto_now=True, help_text='timestamp of last update')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_resume', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ResumeDocType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='resume/candidate/')),
                ('deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='timestamp of creation')),
                ('updated', models.DateTimeField(auto_now=True, help_text='timestamp of last update')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidate_name', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DisputeClaim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_aganist', models.CharField(blank=True, max_length=255, null=True)),
                ('msg', models.TextField(max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='timestamp of creation dispute')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disputeuser', to=settings.AUTH_USER_MODEL)),
                ('dispcause', models.ManyToManyField(help_text='Hold down “Control”, or “Command” on a Mac, to select more than one.', related_name='disputesclaims', to='prof_candidate.DispCause')),
            ],
        ),
        migrations.CreateModel(
            name='Dispute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.TextField(max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='timestamp of creation')),
                ('created_aganist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mcart', to='resumeweb.mcart')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('dispcause', models.ManyToManyField(help_text='Hold down “Control”, or “Command” on a Mac, to select more than one.', related_name='disputes', to='prof_candidate.DispCause')),
            ],
        ),
        migrations.CreateModel(
            name='DeactivatedAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=500)),
                ('confirmation', models.CharField(help_text="Please type 'confirm' ", max_length=7)),
                ('deactivate_status', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='timestamp of creation')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CandidateInternalMsg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(default='Message Subject', max_length=500)),
                ('msg', models.TextField(max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='timestamp of creation')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='msg_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
