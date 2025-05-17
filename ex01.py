import requests
from tinydb import TinyDB
from datetime import datetime
import time


def extract():
    url = "https://api.coinbase.com/v2/prices/spot"

    response = requests.get(url)

    return response.json()
    
def transorm(data):
    value = data['data']['amount']
    currency = data['data']['currency']
    cripto = data['data']['base']
    clean_data = {
        'value': value,
        'cripto': cripto,
        'currency': currency,
        'timestamp': datetime.now().isoformat()
    }
    return clean_data

def load_noSQL(clean_data):
    db = TinyDB('db.json')
    db.insert(clean_data)
    print("Data loaded into the database successfully.")

if __name__ == "__main__":
    while True:
        data = extract()
        clean_data = transorm(data)
        load_noSQL(clean_data)
        time.sleep(15)