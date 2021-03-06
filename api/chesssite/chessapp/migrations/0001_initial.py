# Generated by Django 3.1.13 on 2021-09-29 00:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='untitled', max_length=200)),
                ('description', models.CharField(blank=True, default='untitled', max_length=500)),
                ('move_list', models.CharField(blank=True, default='', max_length=2000)),
                ('white', models.CharField(blank=True, default='stockfish', max_length=200)),
                ('black', models.CharField(blank=True, default='leela', max_length=200)),
                ('time_controls', models.IntegerField(blank=True, default=100)),
                ('results', models.CharField(blank=True, default='*', max_length=10)),
                ('available', models.BooleanField(blank=True, default=True)),
                ('turn', models.CharField(blank=True, default='white', max_length=10)),
                ('fen', models.CharField(blank=True, default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', max_length=200)),
                ('legal_moves', models.CharField(blank=True, default='g1h3,g1f3,b1c3,b1a3,h2h3,g2g3,f2f3,e2e3,d2d3,c2c3,b2b3,a2a3,h2h4,g2g4,f2f4,e2e4,d2d4,c2c4,b2b4,a2a4', max_length=2000)),
                ('pgn', models.CharField(blank=True, default='', max_length=2000)),
                ('creation_date', models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 29, 0, 24, 47, 324991, tzinfo=utc))),
            ],
            options={
                'ordering': ['creation_date'],
            },
        ),
    ]
