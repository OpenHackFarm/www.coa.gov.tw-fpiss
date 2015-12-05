#!/usr/bin/env python
# encoding: utf-8


# Usage:
#    for i in $(seq 1 216); do wget -nc "http://www.coa.gov.tw/fpiss/index.php?page=$i&category=g"; sleep 1; done"
#    python parse_to_csv.py
#    libreoffice g.csv


from bs4 import BeautifulSoup
import csv
import glob

files = glob.glob("*.php*")

with open('g.csv', 'w') as fp:
    csvfile = csv.writer(fp)

    # write header
    csvfile.writerow(('經營業者', '聯絡人', '產品類別', '產品名稱', '所在縣市', '標章資訊', '電話', 'EMAIL'))

    for file in files:
        with open(file, "r") as myfile:
            html_doc = myfile.read().replace('\n', '')

            soup = BeautifulSoup(html_doc, 'html.parser')

            table = soup.find('table', attrs={'bgcolor': "#74CDF8"})
            rows = table.findAll('tr')

            # not write header duplicate
            del rows[0]

            # write rows
            data = {}
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip().encode('utf-8') for ele in cols]

                if(len(cols) > 1):
                    data[u'經營業者'] = cols[0]
                    data[u'聯絡人'] = cols[1]
                    data[u'產品類別'] = cols[2]
                    data[u'所在縣市'] = cols[4]
                    data[u'標章資訊'] = cols[5]
                    data[u'電話'] = cols[6]
                    data[u'EMAIL'] = cols[7]

                    if('...' not in cols[3]):
                        data[u'產品名稱'] = cols[3]
                    else:
                        data[u'產品名稱'] = None
                else:
                    data[u'產品名稱'] = cols[0]

                if(data[u'產品名稱']):
                    csvfile.writerow((data[u'經營業者'], data[u'聯絡人'], data[u'產品類別'],
                        data[u'產品名稱'], data[u'所在縣市'], data[u'標章資訊'],
                        data[u'電話'], data[u'EMAIL']
                        ))
