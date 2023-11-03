import pandas
import pymysql, pymysql.cursors
import backend.Utils.movie_utils as movie_utils
from reusable_imports.common_vars import item_similarity


def get_similar(id, rating):
    sim_score = item_similarity[id] * (rating - 2.5)
    sim_score = sim_score.sort_values(ascending=False)

    return sim_score


def recommend(ids: list, cursor: pymysql.cursors.Cursor):
    ratings = []
    for i in ids:
        recommended = movie_utils.recommend_direct(int(i), 1, cursor)
        ratings.append((str(i), 5))
        ratings.extend([(str(j), 5) for j in recommended])

    recommendations = pandas.DataFrame()
    for i in ratings:

        if i[0] in item_similarity:
            movie_similarity = get_similar(i[0], i[1])
            movie_similarity = movie_similarity.to_frame().T

            recommendations = pandas.concat([recommendations, movie_similarity])

    return list(map(int, list(recommendations.sum().sort_values(ascending=False).to_frame().T.columns)))[:100]
