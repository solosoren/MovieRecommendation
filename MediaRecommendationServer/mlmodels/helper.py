import numpy as np
from sklearn.metrics import mean_squared_error

from media.models import Book, Movie
from ratings.models import BookRatingUser, MovieRatingUser


def run_collaborative_filtering(media_type):
    if media_type == "books":
        num_media, user_params, item_params, ratings, rated = __setup_book_matrices(10)
    else:
        num_media, user_params, item_params, ratings, rated = __setup_movie_matrices(10)

    # reg_params = [0.05, 0.1, 2.5]
    # learning_rates = [0.0001, 0.001, 0.1]
    reg_params = [2.5]
    learning_rates = [0.0001]
    best = [0, 0, 1.0]
    rated_indices = __get_rated_indices(rated)

    i = 0
    for reg_param in reg_params:
        for learning_rate in learning_rates:
            train_ratings, train_rated, val_ratings = __separate_validation_set(i, ratings, rated, rated_indices)

            losses, _, _ = __run_gradient_descent(50, reg_param, learning_rate, user_params, item_params, train_ratings, train_rated)
            print("LOSS:", losses)

            rmse = __compute_rmse(user_params, item_params, ratings)
            print("RMSE:", rmse)

            val_rmse = __compute_val_rmse(user_params, item_params, val_ratings, rated_indices)
            print("VAL RMSE:", val_rmse)

            if val_rmse < best[2]:
                best = [reg_param, learning_rate, val_rmse]

            i += 1
    print("BEST MODEL:", best[0], best[1], best[2])


# After CV, create predictions


def __setup_book_matrices(num_features):
    num_media = Book.objects.count() + 9
    item_params = np.random.rand(num_media, num_features)

    users = BookRatingUser.objects.order_by('id')
    user_params = np.random.rand(users.count(), num_features)

    ratings = np.zeros((num_media, users.count()))
    # Demean: https://beckernick.github.io/matrix-factorization-recommender/
    rated = np.zeros((num_media, users.count()))

    for u in range(users.count()):
        ids = users[u].book_rating_ids.all()

        for r in range(ids.count()):
            book_id = ids[r].id
            rating = users[u].book_ratings[r]

            ratings[book_id, u] = rating
            rated[book_id, u] = 1

    return num_media, user_params, item_params, ratings, rated


def __setup_movie_matrices(num_features):
    movies = Movie.objects.all()
    num_media = movies.count()

    mapping = {}
    for i in range(num_media):
        mapping[movies[i].id] = i

    item_params = np.random.rand(num_media, num_features)

    users = MovieRatingUser.objects.order_by('id')
    user_params = np.random.rand(users.count(), num_features)

    ratings = np.zeros((num_media, users.count()))
    rated = np.zeros((num_media, users.count()))

    for u in range(users.count()):
        ids = users[u].movie_rating_ids.all()

        for r in range(ids.count()):
            movie_id = ids[r].id
            rating = users[u].movie_ratings[r]

            map_id = mapping[movie_id]

            ratings[map_id, u] = rating
            rated[map_id, u] = 1

    return num_media, user_params, item_params, ratings, rated


def __get_rated_indices(rated):
    rated_indices = np.nonzero(rated)
    shuffled_indices = list(zip(rated_indices[0], rated_indices[1]))
    np.random.shuffle(shuffled_indices)
    return shuffled_indices


def __separate_validation_set(i, ratings, rated, rated_indices):
    print(len(rated_indices))
    start = int(0.1 * len(rated_indices) * i)
    end = int(0.1 * len(rated_indices) * (i+1))
    print(0.1 * len(rated_indices) * (i+1))
    print(end)

    val_ratings = []

    train_ratings = ratings.copy()
    train_rated = rated.copy()

    for i in range(start, end):
        x, y = rated_indices[i]

        val_ratings.append(ratings[x, y])

        train_ratings[x, y] = 0
        train_rated[x, y] = 0

    val_ratings = np.array(val_ratings)
    print(val_ratings)

    return train_ratings, train_rated, val_ratings


# MARK: Gradient Descent
def __run_gradient_descent(num_iters, reg_param, learning_rate, user_params, item_params, ratings, rated):
    losses = []

    for i in range(num_iters):
        error = __compute_error(user_params, item_params, ratings, rated)
        item_gradient = __compute_item_gradient(reg_param, error, user_params, item_params)
        user_gradient = __compute_user_gradient(reg_param, error, user_params, item_params)

        loss = __compute_loss(reg_param, error, user_params, item_params)
        losses.append(loss)

        item_params -= learning_rate * item_gradient
        user_params -= learning_rate * user_gradient

    return losses, item_params, user_params


def __compute_error(user_params, item_params, ratings, rated):
    error = np.dot(item_params, user_params.T) - ratings
    return rated * error  # only for rated media


def __compute_item_gradient(reg_param, error, user_params, item_params):
    gradient = np.dot(error, user_params)
    regularization = reg_param * item_params
    return gradient + regularization


def __compute_user_gradient(reg_param, error, user_params, item_params):
    gradient = np.dot(error.T, item_params)
    regularization = reg_param * user_params
    return gradient + regularization


def __compute_loss(reg_param, error, user_params, item_params):
    loss = np.sum(np.square(error)) / 2
    item_regularization = (reg_param / 2) * np.sum(np.square(item_params))
    user_regularization = (reg_param / 2) * np.sum(np.square(user_params))
    return loss + item_regularization + user_regularization


# MARK: TESTING
def __compute_rmse(user_params, item_params, ratings):
    predictions = np.dot(item_params, user_params.T)
    return np.sqrt(mean_squared_error(ratings, predictions)) / len(ratings)


def __compute_val_rmse(user_params, item_params, val_ratings, val_indices):
    all_predictions = np.dot(item_params, user_params.T)
    predictions = []

    for i in range(len(val_indices)):
        x, y = val_indices[i]
        predictions.append(all_predictions[x, y])

    predictions = np.array(predictions)

    return np.sqrt(mean_squared_error(val_ratings, predictions)) / len(predictions)


# MARK: PREDICTIONS
# def __create_predictions(media_type, item_id, user_id):
    # user = models.BookRatingUser(book_ratings=ratings)
    # user.save()
    # user.book_rating_ids.set(book_ids)


# def predict_book(book_id, user_id):
