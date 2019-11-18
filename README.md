# CGJ-RN Web Scraper

Web scraper no site da [Corregedoria Geral de Justiça do RN](https://corregedoria.tjrn.jus.br/) para retornar as informações sobre as secretarias do TJRN presentes nas comarcas do Rio Grande do Norte.

## Como executar

Para rodar basta executar basta rodar o seguinte comando:

```
python app.py
```

Ao executar dessa forma as informações serão exportadas para um arquivo CSV.

Outra opção de exportação é como um arquivo do Excel, para isso bastar passar o flag ```1``` após o nome do arquivo. Da seguinte forma:

```
python app.py 1
```

Os arquivos se encontrarão na pasta ```arquivos```.

## Tecnologias utilizadas

- Python 3.6
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests](https://requests.readthedocs.io/en/master/)
- [Pandas](https://pandas.pydata.org/)
