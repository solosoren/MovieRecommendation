import numpy as np
from media.models import Book, Movie
from userauth.models import BookUser, MovieUser


class CollaborativeFilteringModel(object):
    """ A representation for a CF Model. Use to pass data easier."""
    def __init__(self, media_type):
        if media_type == 'books':
            media = Book.objects.order_by('id')
            users = BookUser.objects.order_by('id')
        else:
            media = Movie.objects.order_by('id')
            users = MovieUser.objects.order_by('id')

        self.media_num = media.count()
        self.users_num = users.count()

        self.mapping = {}
        for i in range(self.media_num):
            self.mapping[media[i].id] = i

        self.ratings = np.zeros((self.media_num, self.users_num))
        self.rated = np.zeros((self.media_num, self.users_num))
        self.ratings_mean = np.array((1, self.media_num))

        self.item_params = np.zeros((1, 1))
        self.user_params = np.zeros((1, 1))

        self.train_ratings = self.ratings.copy()
        self.train_rated = self.rated.copy()
        self.val_indices = []
        self.val_ratings = []
        self.features_num = 0

        self.__import_ratings(media_type, users)

        self.rated_indices = np.nonzero(self.rated)
        self.rated_indices = list(zip(self.rated_indices[0], self.rated_indices[1]))
        np.random.shuffle(self.rated_indices)

    def __import_ratings(self, media_type, users):
        """Import the models ratings.
        Note: Mapping must be set up before calling.
        """
        for u in range(self.users_num):
            rating_objs = users[u].ratings.all()

            for i in range(rating_objs.count()):
                if media_type == 'books':
                    item_id = rating_objs[i].book.id
                else:
                    item_id = rating_objs[i].movie.id

                rating = rating_objs[i].rating

                map_id = self.mapping[item_id]

                self.ratings[map_id, u] = rating
                self.rated[map_id, u] = 1

        self.ratings_mean = np.mean(self.ratings, axis=1)
        self.ratings = self.ratings - self.ratings_mean.reshape(-1, 1)  # De-mean: https://beckernick.github.io/matrix-factorization-recommender/

    def set_user_item_params(self, features_num):
        """Sets the media and user parameters randomly for a given number of features."""
        self.features_num = features_num
        self.item_params = np.random.rand(self.media_num, features_num)
        self.user_params = np.random.rand(self.users_num, features_num)

    def separate_validation_set(self, iteration):
        start = int(0.1 * len(self.rated_indices) * iteration)
        end = int(0.1 * len(self.rated_indices) * (iteration+1))

        self.val_indices = []
        self.val_ratings = []

        for i in range(start, end):
            x, y = self.rated_indices[i]

            self.val_indices.append(self.rated_indices[i])
            self.val_ratings.append(self.ratings[x, y])

            self.train_ratings[x, y] = 0
            self.train_rated[x, y] = 0

        self.val_indices = np.array(self.val_indices)
        self.val_ratings = np.array(self.val_ratings)
