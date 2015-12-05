#!/usr/bin/env python
# encoding: utf-8


# Usage:
#    for i in $(seq 1 57); do wget -nc "http://www.coa.gov.tw/fpiss/index.php?page=$i&category=f"; sleep 1; done"
#    python parse_prod_name.py | sort > f.txt
#    cat f.txt | uniq -c | sort -n


from bs4 import BeautifulSoup
import glob

files = glob.glob("*.php*")

for file in files:
    with open(file, "r") as myfile:
        html_doc = myfile.read().replace('\n', '')

        soup = BeautifulSoup(html_doc, 'html.parser')

        table = soup.find('table', attrs={'bgcolor': "#74CDF8"})
        rows = table.findAll('tr')

        del rows[0]
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip().encode('utf-8') for ele in cols]

            if(len(cols) > 1):
                if('...' not in cols[3]):
                    print cols[3].replace(',', '\n')
            else:
                print cols[0].replace(',', '\n')
