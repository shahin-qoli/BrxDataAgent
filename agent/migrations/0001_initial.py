# Generated by Django 4.0.4 on 2022-05-13 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ocrd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bpcode', models.CharField(blank=True, max_length=200, null=True)),
                ('bpname', models.CharField(blank=True, max_length=200, null=True)),
                ('bpcreatedate', models.DateField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Oslp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slpcode', models.IntegerField()),
                ('slpname', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('desc', models.CharField(max_length=200)),
                ('isactive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vwvisitorsku',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slpcode', models.IntegerField()),
                ('jmonthn', models.IntegerField()),
                ('jyear', models.IntegerField()),
                ('countuniquesku', models.IntegerField()),
                ('countuniquecustomer', models.IntegerField(default=0)),
                ('oslp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.oslp')),
            ],
        ),
        migrations.CreateModel(
            name='Vwcustomerclub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bpcode', models.CharField(max_length=200)),
                ('quarter', models.CharField(max_length=200)),
                ('year', models.CharField(max_length=200)),
                ('numberofinovices', models.IntegerField(blank=True, null=True)),
                ('countsku', models.IntegerField(blank=True, null=True)),
                ('countskuup500kT', models.IntegerField(blank=True, null=True)),
                ('totalprice', models.DecimalField(blank=True, decimal_places=0, max_digits=200, null=True)),
                ('ocrd', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='agent.ocrd')),
            ],
        ),
        migrations.CreateModel(
            name='VwagentActiveCustomerPerVisitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slpcode', models.IntegerField()),
                ('quartern', models.IntegerField()),
                ('activecustomer', models.IntegerField()),
                ('oslp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.oslp')),
            ],
        ),
        migrations.CreateModel(
            name='Ordr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bpcode', models.CharField(max_length=200)),
                ('slpcode', models.IntegerField()),
                ('docdate', models.DateField()),
                ('ocrd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.ocrd')),
                ('oslp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.oslp')),
            ],
        ),
        migrations.CreateModel(
            name='OcrdOslp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bpcode', models.CharField(max_length=200)),
                ('slpcode', models.IntegerField(blank=True, null=True)),
                ('ocrd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.ocrd')),
                ('oslp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agent.oslp')),
            ],
        ),
        migrations.CreateModel(
            name='NewCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bpcode', models.CharField(blank=True, max_length=200, null=True)),
                ('bpcreatedate', models.DateField(blank=True, max_length=200, null=True)),
                ('bpused', models.BooleanField(default=True)),
                ('bpuseddate', models.DateField(blank=True, max_length=200, null=True)),
                ('slpcodeused', models.CharField(blank=True, max_length=200, null=True)),
                ('ocrd', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='agent.ocrd')),
                ('oslp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agent.oslp')),
            ],
        ),
    ]
