import pandas
import pymysql, pymysql.cursors
import utils
import timeit

st = timeit.default_timer()

item_similarity = pandas.read_csv('cos_similarity_upd.csv', index_col=0)

def get_similar(id, rating):
    
    sim_score = item_similarity[id]*(rating-2.5)
    sim_score = sim_score.sort_values(ascending=False)

    return sim_score


def recommend(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    recommended = utils.recommend_direct(id, 1, connection, cursor)
    ratings = [(i, 5) for i in recommended]


    recommendations = pandas.DataFrame()
    for i in ratings:
        
        if i[0] in item_similarity:
            movie_similarity = get_similar(i[0], i[1])
            movie_similarity = movie_similarity.to_frame().T

            recommendations = pandas.concat([recommendations, movie_similarity])

    return list(recommendations.sum().sort_values(ascending=False).to_frame().T.columns)
