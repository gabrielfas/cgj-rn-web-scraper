# -*- coding: utf-8 -*-

# Importando pacotes
import requests
from bs4 import BeautifulSoup
import pandas as pd
import warnings
import sys

warnings.filterwarnings('ignore')

# Recuperando os links dentro das tags <a>
def get_links(a_tags):
	print('Recuperando links...')
	links = []
	# Armazenando os links em uma lista
	for link in a_tags:
		links.append(link.get('href'))
        
	return links

# Recuperando os dados ao acessar os links
def get_dados(links):
	print('Coletando dados...')
	dados = []
	for link in links:
		url_comarca = 'https://corregedoria.tjrn.jus.br' + link

		r = requests.get(url_comarca, verify=False)

		html_comarca = r.text

		soup_comarca = BeautifulSoup(html_comarca)

		comarca = soup_comarca.find_all('h2')[0].text.strip()

		tabelas = [t for t in soup_comarca.find_all('tbody') if 'CHEFE DE SECRETARIA' in t.text]

		for t in tabelas:
			for tr in t.find_all('tr')[1:]:
				linhas = [td for td in tr.find_all('td')]
				valores = [texto.text.strip() for texto in linhas]
				valores.append(comarca)
				dados.append(valores)

	return dados

# Exportando os dados
def exportar_dados(dados, tipo):
	print('Exportando dados...')
	# Convertendo os dados de lista para dataframe
	df_comarcas = pd.DataFrame(dados, columns=['UNIDADE', 'CHEFE DE SECRETARIA', 'TELEFONE', 'COMARCA'])
	# Verificando a flag para saber qual o tipo do arquivo para exportar
	if tipo == 1:
		df_comarcas.to_excel('arquivos/Dados Comarcas TJRN.xlsx', index=False)
	else:
		df_comarcas.to_csv('arquivos/Dados Comarcas TJRN.csv', index=False)
	print('Dados exportados com sucesso!!!')

if __name__ == "__main__":
	print('Iniciando scraping...')

	# Especificando url
	url = 'https://corregedoria.tjrn.jus.br/index.php/judicial/mapa/mapa-judiciario'

	# Inicializando a requisição ao site
	r = requests.get(url, verify=False)

	# Extraindo a resposta como html: html_doc
	html_doc = r.text

	# Criando um objeto BeautifulSoup a partir do HTML: soup
	soup = BeautifulSoup(html_doc)

	# Encontrando todos as tags 'a': a_tags
	a_tags = soup.find_all('a')

	# Chamando a função para recuperar os links da página
	links = get_links(a_tags)

	# Pegando apenas os links de cidades
	links_comarcas = links[links.index('/index.php/acari'):links.index('/index.php/upanema')+1]

	# Chamando a função para trazer os dados do site
	dados_comarcas = get_dados(links_comarcas)
	
	# Checando se a flag é nula
	if len(sys.argv) == 1:
		tipo_arquivo = 0
	else:
		tipo_arquivo = int(sys.argv[1])

	# Chamando a função para exportar os dados
	exportar_dados(dados_comarcas, tipo_arquivo)