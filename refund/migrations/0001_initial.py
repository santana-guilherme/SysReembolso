# Generated by Django 3.1.1 on 2020-10-13 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FinishedQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RefundBundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('state', models.IntegerField(default=0)),
                ('account_number', models.IntegerField(null=True)),
                ('pix', models.CharField(max_length=20, null=True)),
                ('refund_memo', models.ImageField(upload_to='')),
                ('accepting_solicitations', models.BooleanField(default=True)),
                ('object_id', models.PositiveIntegerField(default=1)),
                ('content_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refund', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('name', models.CharField(default='no name', max_length=100)),
                ('price', models.FloatField(default=0)),
                ('state', models.IntegerField(default=0)),
                ('claim_check', models.ImageField(upload_to='claim_checks/')),
                ('queue', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='queue', to='refund.analysisqueue')),
                ('refund_bundle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitations', to='refund.refundbundle')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemSolicitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField(default=0)),
                ('accepted', models.BooleanField(null=True)),
                ('denied_motive', models.CharField(max_length=400, null=True)),
                ('solicitation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='refund.solicitation')),
            ],
        ),
    ]
