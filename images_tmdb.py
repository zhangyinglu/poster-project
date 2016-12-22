from urllib2 import Request, urlopen

api_key = '0ae920f0851bae5f27f82197a85cb729'

def keyword(id):
    headers = {
      'Accept': 'application/json'
    }
    request = Request('http://api.themoviedb.org/3/movie/{}/keywords?api_key={}'.format(id, api_key), headers=headers)
    
    response_body = urlopen(request).read()
    return response_body

def basic(id):
    headers = {
      'Accept': 'application/json'
    }
    request = Request('http://api.themoviedb.org/3/genre/{}/movies?api_key={}'.format(id, api_key), headers=headers)
    
    response_body = urlopen(request).read()
    return response_body

def movie_genre(id):
    headers = {
      'Accept': 'application/json'
    }
    request = Request('http://api.themoviedb.org/3/movie/{}?api_key={}'.format(id, api_key), headers=headers)
    
    response_body = urlopen(request).read()
    return response_body


def reviews(id):
    headers = {
      'Accept': 'application/json'
    }
    request = Request('http://api.themoviedb.org/3/movie/{}/reviews?api_key={}'.format(id, api_key), headers=headers)
    
    response_body = urlopen(request).read()
    return response_body

def imdb2tmdb(id):
    headers = {
      'Accept': 'application/json'
    }
    request = Request('http://api.themoviedb.org/3/find/tt{}?external_source=imdb_id&api_key={}'.format(id, api_key), headers=headers)

    response_body = urlopen(request).read()
    return response_body

def images(id):
    headers = {
      'Accept': 'application/json'
    }
    request = Request('http://api.themoviedb.org/3/movie/{}/images?api_key={}'.format(id, api_key), headers=headers)
    
    response_body = urlopen(request).read()
    return response_body
