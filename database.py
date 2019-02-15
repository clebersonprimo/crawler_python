from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.get_database('imbd')

movie_collection = db.get_collection('movies')
log_collection = db.get_collection('log')
#  Limpa as collections
def drop():
    db.drop_collection('movies')
    db.drop_collection('log')

# Insere os dados coletados do site imdb.com
def insert_fields(data):
    oid = movie_collection.insert(data)
    return oid

#  Insere os erros ocorridos durante a execussão do crawler
def insert_log(data):
    log_collection.insert(data)
    return

#  Lista todos os filmes obtidos pelo crawler
def list_fields():
    return movie_collection.find()

# Busca dos dados de um filme bbaseado em seu id
def get_data_movie(_id):
    return movie_collection.find_one({'id': int(_id)})

#  Log de erros durante a execussão do crawler
def show_log():
    return log_collection.find()

# Contagem total de filmes obtidos pelo crawler
def count_fields():
    total = movie_collection.count()
    return total

# Tempo médio de duração dos filmes
def average_movie_time():
    runtime = 0
    total = movie_collection.count()
    data = movie_collection.find()
    
    for data in movie_collection.find():
        runtime += int(data['runtime'])
    return [runtime, total, runtime /total]

# Média
def average_field(field = None):
    if(field is None):
        field = 'imdb_rating'
    total_rating = 0
    total_movies = movie_collection.count()
    collection = movie_collection.find()
    for data in collection:
        total_rating += float(data[field])
    return total_rating/total_movies

#  Variância
def variance_field(field = None):
    if(field is None):
        field = 'imdb_rating'
    average         = 0
    calc_variance   = 0
    total_movies    = movie_collection.count()
    collection      = movie_collection.find()
    average = average_field(field)

    for data in collection:
        calc_variance += ((float(data[field]) - float(average)) ** 2)
    return calc_variance/total_movies

# Desvio padrão
def std_deviation(field):
    if(field is None):
        field = 'imdb_rating'
    return (variance_field(field) ** 0.5)

# Probabilidade de ser uma mulher a diretora do filme
def prob_female_director():
    woman = movie_collection.find({'dir_gender': 'f'}).count()
    total = movie_collection.count()
    return woman/total

# Probabilidade do filme set nota superior a 8 e seu diretor não ser Americano
def prob_director_evaluation():
    get_american_rate_8 = movie_collection.find({'imdb_rating': {'$gt': '8'}}, {
                                       'is_american': 'false'}).count()
    total = movie_collection.count()
    prob = (get_american_rate_8/total)
    return prob

#  Verificação dos diretores preferidos, baseado na média das notas que seus filmes receberam
def prefer_directors():
    _sum = 0
    total = 0
    result = list()
    directors = movie_collection.distinct('director')

    for director in directors:
        ratings = movie_collection.find({'director': director}, {'imdb_rating'})
        for rating in ratings:
            total += 1
            _sum += float(rating['imdb_rating'])
        result.append({'director': director, 'occur': total, 'rating': _sum })
        total = 0
        _sum = 0


    return sorted(result, key=lambda x: x['rating'], reverse=True)

# Cálculo dos gêneros preferidos utilizando o teorema de Bayes
def genres_evaluations(_id = None):

    total_movie = movie_collection.count()
    _sum = 0
    total = 0
    result = list()
    if not _id:
        genres = movie_collection.distinct('genre')
    else:
        _genres = movie_collection.find_one({'id': int(_id)}, {'genre': 1, '_id': 0})
        genres =  _genres['genre']
    for genre in genres:
        ratings = movie_collection.find({'genre': genre}, {'imdb_rating'})
        for rating in ratings:
            total += 1
            if(float(rating['imdb_rating']) > 8):
                _sum += 1
        pda = ((_sum/total) * (_sum/total_movie)) / \
            ((_sum/total) * (_sum/total_movie) +
             ((1 - (_sum/total)) * (1 - (_sum/total_movie))))
        result.append({'genre': genre, 'occur': total, 'prob' : _sum/total, 'prob_gen' : total/total_movie})
        total = 0
        _sum = 0
    return result
