import unittest
from crawler_imdb import crawler

class VerificaCrawlerTests(unittest.TestCase):
    def test_coletar_dados(self):
        dados_coletados_corretamente = crawler()
        self.assertTrue(dados_coletados_corretamente)
