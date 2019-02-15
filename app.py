from flask import Flask, render_template, request, redirect, jsonify
from crawler_imdb import crawler
from database import *
import json

app = Flask(__name__)

# Definição das rotas da aplicação web
@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    drop()
    return render_template("home.html")

@app.route("/obter_dados")
def obter_dados():
    crawler()
    return redirect('/listar_dados')


@app.route("/listar_dados")
def listar_dados():
    items = list_fields()
    return render_template("listagem_filmes_view.html", items=items)


@app.route("/detalhes")
def detalhes():
    dados = dict()
    _id = request.args.get('id')
    if not _id:
        return "Por favor, informe o id do filme que deseja ver os detalhes"
    dados['filme'] = get_data_movie(_id)
    dados['estatisticas'] = genres_evaluations(_id)
    print(dados)
    return render_template("detalhes_filme_view.html", dados=dados)


@app.route("/generos_preferidos", defaults={'field': None})
@app.route("/generos_preferidos/<field>")
def generos_preferidos(field):
    return render_template("info_genero_view.html", items=genres_evaluations(field))


@app.route("/ver_estatiscicas")
def estatisticas():
    return

@app.route("/total")
def total():
    return 'Total de registros salvos: ' + str(count_fields())

@app.route("/probabilidade")
def probabilidade():
    return jsonify({'prob_female_director': prob_female_director()})


@app.route("/avaliacao_diretor")
def avaliacao_diretor():
    return jsonify({'evaluation_directors': prob_director_evaluation()})


@app.route("/diretores_preferidos")
def diretores_preferidos():
    return jsonify({'favorite_directors': prefer_directors()})



@app.route('/media', defaults={'field': None})
@app.route('/media/<field>')
def media(field):
    return jsonify({'field': field, 'average': average_field(field)})


@app.route('/variancia', defaults={'field': None})
@app.route('/variancia/<field>')
def variancia(field):
    return jsonify({'field': field, 'variance': variance_field(field)})


@app.route('/desvio_padrao', defaults={'field': None})
@app.route('/desvio_padrao/<field>')
def desvio_padrao(field):
    return jsonify({'field': field, 'std_deviation': std_deviation(field)})


@app.route('/log_erros')
def log_erros():
    erros = show_log()
    if not erros:
        return "Nenhum erro foi registrado durante a obtenção dos dados"
    else:
        return render_template("erros_view.html", erros=erros)

if __name__ == '__main__':
    app.run(debug=True)


