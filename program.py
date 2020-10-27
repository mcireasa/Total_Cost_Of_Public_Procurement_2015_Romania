from os.path import split
import urllib.request, csv, os, json, requests, re
from datetime import datetime
from bs4 import BeautifulSoup

url = 'https://data.gov.ro/datastore/dump/9e0f19f1-b4ce-4f27-b5ec-6f644145e7f3?bom=True'

if not os.path.exists("./2015.csv"):
    urllib.request.urlretrieve(url, "./2015.csv")


def creare_dictionare():
    dict_judete = {}
    with open('2015.csv', mode = 'r') as csv_open1:
        csv_header1 = csv.reader(csv_open1, delimiter = ",")
        for linie1 in csv_header1: 
            dict_judete.update({linie1[6]: ''})
    del dict_judete["Judet"]
    for judet in dict_judete.keys():
        sum = 0
        with open("2015.csv", mode = 'r') as csv_open2:
            csv_reader2 = csv.reader(csv_open2, delimiter = ",")
            for linie2 in csv_reader2:
                if judet == linie2[6]:
                    sum += float(linie2[11])
            dict_judete[judet] = sum
    return dict_judete

dictionar = creare_dictionare()


def scriere_csv(dict):
    if not os.path.exists("./valori.csv"):
        with open('valori.csv', mode='w') as csv_header:
            csv_header_writer = csv.writer(csv_header)
            csv_header_writer.writerow(["Judet", "Valoare Estimata"])
    ok = 0
    with open('valori.csv', mode='r') as check_header:
        csv_check_header = csv.reader(check_header)
        row_count = 0
        lista = list(csv_check_header)
        for row in lista:
            row_count += 1
        if(row_count == 1):
            ok = 1
    if (ok == 1):
        with open('valori.csv', mode = 'a') as csv_row:
            csv_row_writer = csv.writer(csv_row)
            for judet,suma in dict.items():
                csv_row_writer.writerow([judet, suma])

scriere_csv(dictionar)


def export_to_json():
    dict_contracte = {}
    for month in range(1,13):
        dict_contracte.update({month: ''})
        for luna in dict_contracte.keys():
            sum = 0
            with open('2015.csv', mode = 'r') as csv_open5:
                csv_reader5 = csv.reader(csv_open5, delimiter = ",")
                next(csv_reader5)
                for linie5 in csv_reader5:
                    year,month,rest = (linie5[3].split('-'))
                    if luna == int(month):
                        sum += float(linie5[11])
                dict_contracte[luna] = sum
    json_obj = json.dumps(dict_contracte, indent = 3)
    with open('valori.json', 'w') as json_out:
        json_out.write(json_obj)


export_to_json()

def preiat_curs_valutar():
    currency_url = "https://www.bnr.ro/nbrfxrates.xml"
    index_page = requests.get(currency_url)
    soup = BeautifulSoup(index_page.text, 'html.parser')
    dict_monede = soup.find_all('rate')
    return dict_monede


dict_monede = preiat_curs_valutar()



def convertor(suma, moneda):
    if(len(moneda) > 3):
        print("Moneda nu trebuie sa aiba mai mult de 3 caractere....")
    moneda = moneda.upper()
    valoare_ron = 0
    valori = [valoare.get_text() for valoare in dict_monede]
    monede = []
    monede_raw = re.findall("[<rate currency=\"][A-Z]{3}", str(dict_monede))
    for moneda_raw in monede_raw:
        moneda_buna = re.split("\"", str(moneda_raw))
        monede.append(moneda_buna[1])
    for verificare_moneda in monede:
        if moneda == verificare_moneda:
            curs_valutar = valori[monede.index(moneda)]
            valoare_ron = float(suma) * float(curs_valutar)
    return valoare_ron


def corectare_valori():
    if not os.path.exists('./valori_ron.csv'):
        with open('valori_ron.csv', mode = 'w') as csv_header: 
            csv_header_writer = csv.writer(csv_header)
            csv_header_writer.writerow(["Judet", "Valoare Estimata"])
    valori_csv = list()
    with open('2015.csv', mode = 'r') as csv_open6:
        csv_reader6 = csv.reader(csv_open6, delimiter=',')
        valori_csv = list(csv_reader6)
    for linie1 in valori_csv:
        if "EUR" == linie1[12]:
            linie1[11] = convertor(linie1[11],"EUR")
    for linie2 in valori_csv:
        if "USD" == linie2[12]:
            linie2[11] = convertor(linie2[11],"USD")
    dict_ron = {}
    with open('2015.csv', mode='r') as csv_open7:
        csv_reader7 = csv.reader(csv_open7, delimiter=",")
        for lini3 in csv_reader7:
            dict_ron.update({lini3[6]:''})
    del dict_ron["Judet"]
    for judet in dict_ron.keys():
        sum = 0
        for linie4 in valori_csv:
            if judet == linie4[6]:
                sum += float(linie4[11])
                dict_ron[judet] = sum
    with open('valori_ron.csv', mode="a") as valori_ron:
        valori_ron_writer = csv.writer(valori_ron, delimiter=',')
        for judet, suma in dict_ron.items():
            valori_ron_writer.writerow([judet, suma])


corectare_valori()




