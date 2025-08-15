import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import create_app
from app.models import db, CovidCase

app = create_app()

print("--- Iniciando o script de seeding ---")

DATABASE_URL =  os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise Exception("A variável de ambiente DATABASE_URL não está definida.")

print(f"Conectando ao banco de dados...")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

try:
    with app.app_context():
        print("Garatindo que a tabela 'covid_cases' existe...")
        db.create_all()
        print("Tabela verificada com sucesso.")
    
    
    existing_data_count = session.query(CovidCase).count()
    if existing_data_count > 0:
        print(f"O banco de dados já contém {existing_data_count} registros. A sair.")
        exit()

        
    print("Lendo o ficheiro covid_data.csv...")
    df = pd.read_csv('/data/covid_data.csv')
    df.rename(columns={'date': 'report_date', 'country': 'country', 'cases': 'cases', 'deaths': 'deaths'}, inplace=True)
    print(f"Encontrados {len(df)} registros no CSV. Processando...")
    
    
    records_to_insert = df.to_dict(orient='records')
    session.bulk_insert_mappings(CovidCase, records_to_insert)
    
    print("Inserindo os dados no banco de dados...")
    session.commit()
    print(f"--- Sucesso! {len(records_to_insert)} registros foram adicionados ao banco de dados. ---")
    
except Exception as e:
    print(f"Ocorreu um erro: {e}")
    session.rollback()
finally:
    session.close()
    print("--- Script de seeding finalizado. ---")