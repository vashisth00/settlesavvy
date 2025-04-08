# Generated by Django 4.2 on 2025-04-08 21:51

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Factors',
            fields=[
                ('factor_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('source', models.CharField(max_length=255)),
                ('default_scoring_strategy', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GeoFactors',
            fields=[
                ('geo_factor_id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.FloatField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('needs_fetch', models.BooleanField(default=True)),
                ('factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settlesavvy_core.factors')),
            ],
        ),
        migrations.CreateModel(
            name='Geographies',
            fields=[
                ('geo_id', models.CharField(default='0000000', max_length=20, primary_key=True, serialize=False)),
                ('geo_type', models.CharField(default='unspecified', max_length=50)),
                ('name', models.CharField(default='Unnamed', max_length=255)),
                ('namelsad', models.CharField(default='Unnamed Area', max_length=255)),
                ('aland', models.BigIntegerField(default=0)),
                ('awater', models.BigIntegerField(default=0)),
                ('intptlat', models.DecimalField(decimal_places=7, default=0.0, max_digits=9)),
                ('intptlon', models.DecimalField(decimal_places=7, default=0.0, max_digits=10)),
                ('geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Geographies',
            },
        ),
        migrations.CreateModel(
            name='Maps',
            fields=[
                ('map_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_stamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('center_point', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
                ('zoom_level', models.FloatField()),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='maps', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MapGeos',
            fields=[
                ('map_geo_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('geo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settlesavvy_core.geographies')),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settlesavvy_core.maps')),
            ],
        ),
        migrations.CreateModel(
            name='MapFactors',
            fields=[
                ('map_factor_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('weight', models.FloatField()),
                ('scoring_strategy', models.CharField(default='no_scoring', max_length=50)),
                ('filter_strategy', models.CharField(default='no_filter', max_length=50)),
                ('score_tipping_1', models.FloatField(blank=True, null=True)),
                ('score_tipping_2', models.FloatField(blank=True, null=True)),
                ('filter_tipping_1', models.FloatField(blank=True, null=True)),
                ('filter_tipping_2', models.FloatField(blank=True, null=True)),
                ('created_stamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settlesavvy_core.factors')),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settlesavvy_core.maps')),
            ],
        ),
        migrations.CreateModel(
            name='MapFactorGeos',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('aggregate_score', models.FloatField()),
                ('geo_factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settlesavvy_core.geofactors')),
                ('map_factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settlesavvy_core.mapfactors')),
                ('map_geo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settlesavvy_core.mapgeos')),
            ],
        ),
        migrations.AddField(
            model_name='geofactors',
            name='geo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settlesavvy_core.geographies'),
        ),
        migrations.AlterUniqueTogether(
            name='geofactors',
            unique_together={('factor', 'geo')},
        ),
    ]
