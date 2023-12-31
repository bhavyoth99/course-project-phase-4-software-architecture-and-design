# Generated by Django 4.2.4 on 2023-08-25 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(choices=[(1, 'K-2'), (2, '3-5'), (3, '6-8')], default=1)),
                ('pattern', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100)),
                ('hand', models.CharField(max_length=255)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.game')),
            ],
        ),
        migrations.CreateModel(
            name='Turn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cards_played', models.CharField(max_length=255)),
                ('is_successful', models.BooleanField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.player')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suit', models.CharField(choices=[('hearts', 'Hearts'), ('diamonds', 'Diamonds'), ('clubs', 'Clubs'), ('spades', 'Spades')], max_length=10)),
                ('rank', models.CharField(choices=[('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('J', 'J'), ('Q', 'Q'), ('K', 'K'), ('A', 'A')], max_length=2)),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.game')),
            ],
        ),
    ]
