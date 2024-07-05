import tmdbsimple as tmdb

tmdb.API_KEY = '10af8f144bffa38b9fc3a0ced21b52af'

def search(phrase: str, search: tmdb.Search) -> list[dict]:
    """
    search for movies using `phrase`
    """

    search.movie(query = phrase)
    return search.results