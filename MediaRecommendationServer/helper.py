import sys
import os
import django
from django.conf import settings


def import_movie_ratings():
    """Imports the data at the given path to a csv file."""
    path = './movie_ratings.csv'
    with open(path, 'r') as f:
        uid = 1
        user = MovieUser(id=uid)
        user.save()

        for line in f:
            terms = line.strip().split(',')

            if terms[0] != uid and terms[1] != str(62437):
                uid = terms[0]
                user = MovieUser(id=uid)
                user.save()

                rating = MovieRating(rating_user=user,
                                     movie=Movie.objects.get(id=int(terms[1])),
                                     rating=float(terms[2]))
                rating.save()

            elif terms[1] != str(62437):
                rating = MovieRating(rating_user=user,
                                     movie=Movie.objects.get(id=int(terms[1])),
                                     rating=float(terms[2]))
                rating.save()


def import_book_ratings():
    path = './book_ratings.csv'
    with open(path, 'r') as f:
        uid = 1
        csv_uid = 1
        user = BookUser(id=uid)
        user.save()

        for line in f:
            terms = line.strip().split(',')

            if terms[0] != csv_uid and terms[1] != str(3618):
                csv_uid = terms[0]
                uid += 1

                user = BookUser(id=uid)
                user.save()

                rating = BookRating(rating_user=user,
                                    book=Book.objects.get(id=int(terms[1])),
                                    rating=float(terms[2]))
                rating.save()

            elif terms[1] != str(3618):
                rating = BookRating(rating_user=user,
                                    book=Book.objects.get(id=int(terms[1])),
                                    rating=float(terms[2]))
                rating.save()


# def update_movie_ids():
#     movies = Movie.objects.all()
#     num_media = movies.count()
#
#     mapping = {}
#     for i in range(num_media):
#         mapping[movies[i].id] = i
#
#     users = MovieRatingUser.objects.order_by('id')

    # for user in users:


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediaRecommendationServer.settings")

    django.setup()
    from MediaRecommendationServer import *
    import mlmodels.helper as ml
    from media.models import Movie, Book
    from userauth.models import MovieUser, BookUser
    from ratings.models import MovieRating, BookRating

    if sys.argv[1] == "import_book_ratings":
        import_book_ratings()

    elif sys.argv[1] == "import_movie_ratings":
        import_movie_ratings()

    elif sys.argv[1] == "run_book_ml":
        ml.run_collaborative_filtering('books')

    elif sys.argv[1] == "run_movie_ml":
        ml.run_collaborative_filtering('movies')
