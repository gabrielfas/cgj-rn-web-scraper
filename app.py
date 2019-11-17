# -*- coding: utf-8 -*-

# Import packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import warnings
import sys

warnings.filterwarnings('ignore')

# Getting the links inside the tags <a>
def get_links(a_tags):
	print('Recuperando links...')
	links = []
	# Appending the links to a list
	for link in a_tags:
		links.append(link.get('href'))
	return links

# Getting the data from the links
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

# Exporting the data into a csv file
def exportar_dados(dados, tipo):
	print('Exportando dados...')
	# Converting data into a pandas object
	df_comarcas = pd.DataFrame(dados, columns=['UNIDADE', 'CHEFE DE SECRETARIA', 'TELEFONE', 'COMARCA'])
	# Checking which file extension to export
	if tipo == 1:
		df_comarcas.to_excel('outputs/Dados Comarcas TJRN.xlsx', index=False)
	else:
		df_comarcas.to_csv('outputs/Dados Comarcas TJRN.csv', index=False)
	print('Dados exportados com sucesso!!!')

if __name__ == "__main__":
	print('Iniciando scraping...')

	# Specify url
	url = 'https://corregedoria.tjrn.jus.br/index.php/judicial/mapa/mapa-judiciario'

	# Package the request, send the request and catch the response: r
	r = requests.get(url, verify=False)

	# Extracts the response as html: html_doc
	html_doc = r.text

	# create a BeautifulSoup object from the HTML: soup
	soup = BeautifulSoup(html_doc)

	# Find all 'a' tags (which define hyperlinks): a_tags
	a_tags = soup.find_all('a')

	# Calling get_links function
	links = get_links(a_tags)

	# Slicing all links to get only the cities links
	links_comarcas = links[links.index('/index.php/acari'):links.index('/index.php/upanema')+1]

	#print(links_comarcas)

	# Calling get_dados function
	dados_comarcas = get_dados(links_comarcas)
	
	# Checking if command line is null
	if len(sys.argv) == 1:
		tipo_arquivo = 0
	else:
		tipo_arquivo = int(sys.argv[1])

	# Calling exportar_dados function
	exportar_dados(dados_comarcas, tipo_arquivo)