import runpy
import sqlite3
import pandas as pd
from config import TABLES,DATABASE_PATH,LOCAL_PATH

runpy.run_path(path_name='ETL/extract.py')

def load_data(tables,db_path):

    conn = sqlite3.connect(db_path)
    print("Connect")
    
    for file in tables:
        df = pd.read_csv(LOCAL_PATH + file + ".csv")
        df.to_sql(file,conn,if_exists='replace',index=False)
        print(f"{file} loaded")

    conn.commit()
    conn.close()

load_data(TABLES,DATABASE_PATH)