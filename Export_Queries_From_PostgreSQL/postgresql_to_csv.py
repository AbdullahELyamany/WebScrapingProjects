from sqlalchemy import create_engine
import pandas as pd


engine = create_engine('postgresql://postgres:postg1344@localhost/Cryptocurrency')

df = pd.read_sql_query('SELECT * FROM crypto', engine)

engine.dispose()

df.to_csv('cryptocurrency.csv', index=False)
