#!/usr/bin/env python3

import json
import requests
from pywebio import start_server
from pywebio.output import put_table
from pywebio.input import select

# pip3 install pywebio requests

url = "https://api.coincap.io/v2/assets"
dic = {}


def reload():
    global x
    try:
        req = requests.get(url)
        x = json.loads(req.text)
    except:
        print("exit")
        exit(0)
  
  
def data():
    global options
    reload()
    values = []
    for y in range(len(x['data'])):
        values.append(x['data'][y]['symbol'])
        symbol = x['data'][y]['symbol']
        price = x['data'][y]['priceUsd']
        dic[str(symbol)] = price
    options = sorted(values)
    return(dic)


def makeusd(cash):
    x = cash.startswith("0.00")
    if x == True:
        usd = f"${cash}"
    else:
        usd = '${:,.2f}'.format(float(cash))
    return(usd)


def main():
    while True:        
        all = data()
        symbol = select("Select a coin:", options)     
        if symbol in all:
            put_table([
                ['Crypto:', symbol,],
                ['Value:', makeusd(str(all[symbol]))]
            ])            
        else:
            print("Key exists isn't in the dictionary.")
            exit    


if __name__ == '__main__':
    start_server(main, port=8090, debug=True)
