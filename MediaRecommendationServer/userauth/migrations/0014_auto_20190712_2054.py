# Generated by Django 2.2.2 on 2019-07-12 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0013_auto_20190711_1606'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='book_uid',
            new_name='book_user',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='movie_uid',
            new_name='movie_user',
        ),
    ]
