# Generated by Django 2.2.2 on 2019-08-03 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0008_auto_20190712_2054'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['-average_rating', '-num_watched', 'title']},
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['-average_rating', '-num_watched', 'title']},
        ),
        migrations.AddField(
            model_name='book',
            name='num_watched',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='num_watched',
            field=models.IntegerField(default=0),
        ),
    ]
