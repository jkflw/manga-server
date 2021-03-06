# Generated by Django 2.1.3 on 2020-02-12 05:34

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_page_size', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WatchedSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='directory',
            name='authors',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, db_index=True, default='', size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='directory',
            name='completely_scanlated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='directory',
            name='genres',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, db_index=True, default='', size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='directory',
            name='manga_image',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='directory',
            name='manga_updates_link',
            field=models.TextField(db_index=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='directory',
            name='related_series',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, db_index=True, default='', size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='directory',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, db_index=True, default='', size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='directory',
            name='title',
            field=models.TextField(db_index=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='directory',
            name='year',
            field=models.TextField(db_index=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='watchedseries',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manga.Directory'),
        ),
    ]
