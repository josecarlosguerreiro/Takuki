import urllib.request
from bs4 import BeautifulSoup
import ssl
import takuki as takuki

row_list = []

def openURL(url, contador):
    if contador == 0:
        row_list = []
    else:
        pass

    ssl._create_default_https_context = ssl._create_unverified_context
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    html = mybytes.decode("utf8")
    fp.close()
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    table_rows = tables[0].find_all('tr')
    #print(table_rows)
    row_list.append(table_rows)
    #print("HTML: " + str(html))
    if html.__contains__('{page}'):
        #print('NUMERO DE PAGINAS --> ' + str(html.count('{page}')))
        contador = html.count('{page}')
        for i in range(2, html.count('{page}') + 1):
           url = url + '/page/' + str(i)
           #print("abrir pagina 2")
           #print("url --> " + url)
           table_rows_2 = abreURLCompleto(url)
           row_list.append(table_rows_2)
    return row_list

def abreURLCompleto(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    html = mybytes.decode("utf8")
    fp.close()
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    table_rows = tables[0].find_all('tr')
    return table_rows
