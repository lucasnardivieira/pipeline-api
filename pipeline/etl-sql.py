import requests
from tinydb import TinyDB
from datetime import datetime
import time
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Configurando o banco de dados SQL, dentro do Render
DATABASE_URL = os.getenv("DATABASE_URL")

# Criação do engine e da sessão
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Modelo de dados
class BitcoinData(Base):
    __tablename__ = 'bitcoin_data'
    id = Column(Integer, primary_key=True)
    value = Column(Float)
    cripto = Column(String(10))
    currency = Column(String(10))
    timestamp = Column(DateTime)

# Criação da tabela
Base.metadata.create_all(engine)

def extract():
    url = "https://api.coinbase.com/v2/prices/spot"

    response = requests.get(url)

    return response.json()
    
def transorm(data):
    value = float(data['data']['amount'])
    currency = data['data']['currency']
    cripto = data['data']['base']
    clean_data = BitcoinData(
        value=value,
        cripto=cripto,
        currency=currency,
        timestamp=datetime.now()
    )
    return clean_data

def load_SQL(clean_data):
    with Session() as session:
        session.add(clean_data)
        session.commit()
        print("Data loaded into PostgreSQL successfully.")    

if __name__ == "__main__":
    while True:
        data = extract()
        clean_data = transorm(data)
        load_SQL(clean_data)
        time.sleep(15)