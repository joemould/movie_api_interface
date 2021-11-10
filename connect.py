import sys
import requests
import pandas as pd

# should be allowed to specify movie search string in cli and this does the rest for you
# build functionality when required not for the sake of it

api_key = "f8b8c7ff9bdb10d377dbf69f1d19dfce"
base_url = "https://api.themoviedb.org/3"

def run(movie_query):
    movie_search_endpoint = "/search/movie"
    movie_search_url =  "{}{}?api_key={}&query={}".format(base_url, movie_search_endpoint, api_key, movie_query)

    r = requests.get(movie_search_url)

    if r.status_code in range(200,299):
        data = r.json()
        results = data['results']
        if len(results) > 0:
            movie_ids = set()
            for result in results:
                _id = result['id']
                print(result['title'], _id)
                movie_ids.add(_id)
            print(list(movie_ids))

    output = 'movies.csv'
    movie_data = []

    for movie_id in movie_ids:
        movie_by_id_endpoint = "/movie/{}".format(movie_id)
        movie_by_id_url = "{}{}?api_key={}".format(base_url, movie_by_id_endpoint, api_key)
        r = requests.get(movie_by_id_url)
        print(r.status_code)
        print(r.text)
        if r.status_code in range(200,299):
            movie_data.append(r.json())

    # TODO combine data from multiple sources - web scraping tool

    df = pd.DataFrame(movie_data)
    print(df.head())
    df.to_csv(output, index=False)


if __name__ == '__main__':
    # TODO use python click to parse args and validate
    assert len(sys.argv) == 2
    movie_query = sys.argv[1]
    run(movie_query)