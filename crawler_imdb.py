import requests
from database import insert_fields, insert_log
from bs4 import BeautifulSoup
import re

# Função crawler que realiza as requisições à página IMDB para obtenção de dados de filmes.
def crawler():
    # Definição do número de páginas que serão percorridas para obtenção dos dados. 
    # Como a página lista os filmes de 50 em 50, o número total de filmes
    # será a soma do número total de páginas visitadas multiplicado por 50, no caso 5000.
    pages = [str(i) for i in range(1, 101)]
    count = 1
    result = True
    for page in pages:
        url = 'https://www.imdb.com/search/title?title_type=feature&user_rating=1.0,10.0&has=business-info,x-ray&start=' + page
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            insert_log({'step': 'get request', 'success': False, 'exception': str(e)})
            return 'Error: ' + str(e)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        if(html_soup == ''):
            insert_log({'step': 'html_soup', 'success': False, 'exception': 'Page not found'})
            return 'Error: A página solicitada não foi encontrada'

        movie_containers = html_soup.find_all('div', class_ = 'lister-item-content')
        if(not movie_containers):
            insert_log({'step': 'movie_containers', 'success': False, 'exception': 'The page requested does not match the IMDB page'})
            return 'Error: A URL solicitada não corresponde com a página do IMDB'

        #Função que extrai as informações da página
        # Após a obtenção dos dados de cada filme, os mesmos são padronizados no formato json e salvo em banco de dados mongodb
        for container in movie_containers:
            #Obtenção dos dados contidos no bloco principal:
            #Título do filme, ano de lançamento, tempo de duração
            header  = container.find('h3', class_ = 'lister-item-header')
            title   = header.find('a', href=True).text
            year    = header.find('span', class_ = 'lister-item-year text-muted unbold').text
            runtime = container.find('span', class_='runtime').text.strip(' min')
            # Afim de manter a consistência dos dados, ignora-se os filmes que não possuem informação de tempo de duração
            if runtime == '':
                continue
            # Obtenção dos demais dados que se encontram no corpo do bloco analisado
            genre           = list(filter(None, container.find('span', class_='genre').text.strip().split(', ')))
            info            = container.find_all('p')
            director        = list(filter(None, info[2].text.split('\n')[2].split(', ')))
            dir_nacionality = get_director_nacionality(info[2].text.split('\n')[2])
            director_gender = get_director_gender(info[2].text.split('\n')[2])
            match           = re.search('([0-9]+)', year)
            year            = year[match.start() : match.end()]
            rating          = container.strong.text.strip()
            other_infos     = container.find('p', class_='sort-num_votes-visible')
            num_votes       = other_infos.find_all('span', {'data-value': True})[0]['data-value']
            gain            = other_infos.find_all('span', {'data-value': True})[1]['data-value']

            try:
                insert_fields({'id': count, 'title': title, 'year': year, 'runtime': runtime,
                                'genre': genre, 'director': director, 'is_american': dir_nacionality,
                                'dir_gender': director_gender, 'votes': num_votes, 'gain': gain, 'imdb_rating': rating})
            except Exception as e:
                insert_log({'url': 'insert_field', 'success': False,
                            'exception': str(e)})
                result = False
                break
            count += 1
    return result

# Definição da nacionalidade do Diretor do filme, verifica se o mesmo é Amoericano ou não
def get_director_nacionality(name):
    director_request = requests.get(
        'https://www.imdb.com/search/name?birth_place=usa&name=' + name.replace(' ', '+'))
    director_soup = BeautifulSoup(director_request.text, 'html.parser')
    if(director_soup.find('div', class_='lister-item-content') is None):
        return 'false'
    else:
        return 'true'

# Definição do sexo do(a) diretor(a) do filme
def get_director_gender(name):
    director_request = requests.get(
        'https://www.imdb.com/search/name?bio=she&name=' + name.replace(' ', '+'))
    director_soup = BeautifulSoup(director_request.text, 'html.parser')
    if(director_soup.find('div', class_='lister-item-content') is None):
        return 'm'
    else:
        return 'f'

# crawler()
