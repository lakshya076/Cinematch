import pandas
import pymysql, pymysql.cursors
import backend.Utils.movie_utils as movie_utils

def get_similar(id, rating, sim_table: pandas.DataFrame):
    sim_score = sim_table[id] * (rating - 2.5)
    sim_score = sim_score.sort_values(ascending=False)

    return sim_score


def recommend(ids: list, cursor: pymysql.cursors.Cursor, sim_table: pandas.DataFrame):
    ratings = []
    recommends = []
    for i in ids:
        recommended = movie_utils.recommend_direct(int(i), 1, cursor)
        recommends.extend(recommended)
        ratings.append((str(i), 5))
        ratings.extend([(str(j), 5) for j in recommended])

    recommendations = pandas.DataFrame()
    for i in ratings:
        if i[0] in sim_table:
            
            movie_similarity = get_similar(i[0], i[1], sim_table)
            movie_similarity = movie_similarity.to_frame().T

            recommendations = pandas.concat([recommendations, movie_similarity])

    recom = list(map(int, list(recommendations.sum().sort_values(ascending=False).to_frame().T.columns)))[:100]
    result = recommends
    result.extend([int(i) for i in recom if i not in result])
    print(result)
    return result
