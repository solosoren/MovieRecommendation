# Generated by Django 2.2.2 on 2019-07-03 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0011_auto_20190703_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movieratinguser',
            name='movie_rating_ids',
        ),
        migrations.AlterField(
            model_name='user',
            name='book_uid',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='ratings.BookRatingUser'),
        ),
        migrations.AlterField(
            model_name='user',
            name='movie_uid',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='ratings.MovieRatingUser'),
        ),
        migrations.DeleteModel(
            name='BookRatingUser',
        ),
        migrations.DeleteModel(
            name='MovieRatingUser',
        ),
    ]
