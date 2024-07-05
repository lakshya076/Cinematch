import tmdbsimple as tmdb

def search(phrase: str, search: tmdb.Search) -> list[dict]:
    """
    search for movies using `phrase`
    """

    search.movie(query = phrase)
    return search.results