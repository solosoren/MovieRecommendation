# Generated by Django 2.2.2 on 2019-07-10 04:45

from django.db import migrations, models
from sortedm2m.operations import AlterSortedManyToManyField
from sortedm2m.fields import SortedManyToManyField
# from media.models import Movie, Book


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0007_auto_20190701_1600'),
        ('ratings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movieratinguser',
            name='predictions',
            field=models.ManyToManyField(related_name='ordered_predictions', to='media.Movie'),
        ),
        AlterSortedManyToManyField(model_name='movieratinguser',
                                   name='predictions',
                                   field=SortedManyToManyField('media.Movie', related_name='ordered_predictions'),
        ),
        AlterSortedManyToManyField(model_name='movieratinguser',
                                   name='movieratingids',
                                   field=SortedManyToManyField('media.Movie'),
        ),
        AlterSortedManyToManyField(model_name='bookratinguser',
                                   name='bookratingids',
                                   field=SortedManyToManyField('media.Book'),
        ),
    ]