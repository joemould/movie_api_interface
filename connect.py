import sys
import os
import requests
import pandas as pd


BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')

api_key = "f8b8c7ff9bdb10d377dbf69f1d19dfce"
base_url = "https://api.themoviedb.org/3"


def get_movies_by_searchstr(query):
    movie_search_endpoint = "/search/movie"
    movie_search_url =  "{}{}?api_key={}&query={}".format(base_url, movie_search_endpoint, api_key, query)

    r = requests.get(movie_search_url)
    if r.status_code not in range(200,299):
        r.raise_for_status()

    results = r.json()['results']
    if not len(results):
        print("No results from search query={}.".format(query))
        return
    movie_ids = set()
    for result in results:
        _id = result['id']
        movie_ids.add(_id)

    movie_data = []
    for movie_id in movie_ids:
        movie_by_id_endpoint = "/movie/{}".format(movie_id)
        # TODO create a function to construct url including kwargs to be reused at top of run
        movie_by_id_url = "{}{}?api_key={}".format(base_url, movie_by_id_endpoint, api_key)
        r = requests.get(movie_by_id_url)
        if r.status_code in range(200,299):
            movie_data.append(r.json())

    if not len(movie_data):
        print("No movie data found for movie_ids {}.".format(movie_ids))
        return

    # TODO combine data from multiple sources - web scraping tool
    os.makedirs(DATA_DIR, exist_ok=True)
    output_filename = "{}-movies.csv".format(query)
    output_filepath = os.path.join(DATA_DIR, output_filename)
    print("Saving csv to {}".format(output_filepath))
    df = pd.DataFrame(movie_data)
    print(df.head())
    df.to_csv(output_filepath, index=False)


if __name__ == '__main__':
    # TODO use python click to parse args and validate
    assert len(sys.argv) == 2
    movie_query = sys.argv[1]
    get_movies_by_searchstr(movie_query)