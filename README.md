Crawler desenvolvido em Python, com armazenamento em mongodb, para a busca de informações da base de dados de filmes do IMDB.


### Rodar o ambiente Docker
```
docker-compose build
```

```
docker-compose up
```
Para atestar o funcionamento da aplicação acesse `localhost:5000`

### Executar os testes
```
python -m unittest test_coletar_dados
```
* Acesse `localhost:5000/obter_dados` para extrair as informações da base de dados
* Para acessar mais informações a respeito de um título específico acesse `localhost:5000/detalhes?id=`
* Para verificar a ocorrência de erros na busca dos dados acesse `localhost:5000/log_erros`
