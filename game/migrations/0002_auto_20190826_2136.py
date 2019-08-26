# Generated by Django 2.2.4 on 2019-08-26 21:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='history1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='history2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='history3',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterIndexTogether(
            name='game',
            index_together={('player', 'history1', 'history2', 'history3'), ('player', 'created'), ('history1', 'history2', 'history3')},
        ),
    ]