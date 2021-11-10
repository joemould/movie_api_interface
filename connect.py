import requests
import pandas as pd

api_key_v3 = "f8b8c7ff9bdb10d377dbf69f1d19dfce"
# api_key_v4 = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmOGI4YzdmZjliZGIxMGQzNzdkYmY2OWYxZDE5ZGZjZSIsInN1YiI6IjYxOGJlZGJlY2I2ZGI1MDA4ZDYwYzFhMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.qtxKp38FOFPUVxArqJYl9M7JLwNq8zT5eDuqsIkH3m4"

api_version = 3
api_base_url = "https://api.themoviedb.org/{}".format(api_version)

movie_id = 503
movie_by_id_endpoint = "/movie/{}".format(movie_id)
movie_by_id_url = "{}{}?api_key={}".format(api_base_url, movie_by_id_endpoint, api_key_v3) # v3
# movie_by_id_url = "{}{}".format(api_base_url, movie_endpoint) # v4

movie_search_endpoint = "/search/movie"
movie_query = "Fight"
movie_search_url =  "{}{}?api_key={}&query={}".format(api_base_url, movie_search_endpoint, api_key_v3, movie_query) # v3

# headers = {
#     'Authorization': 'Bearer {}'.format(api_key_v4),
#     'Content-Type': 'application/json;charset=utf-8'
# } # v4


r = requests.get(movie_search_url) # v3
# r = requests.get(movie_url, headers=headers) # v4

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
    movie_by_id_url = "{}{}?api_key={}".format(api_base_url, movie_by_id_endpoint, api_key_v3)
    r = requests.get(movie_by_id_url)
    print(r.status_code)
    print(r.text)
    if r.status_code in range(200,299):
        movie_data.append(r.json())

# TODO combine data from multiple sources - web scraping tool

df = pd.DataFrame(movie_data)
print(df.head())
df.to_csv(output, index=False)