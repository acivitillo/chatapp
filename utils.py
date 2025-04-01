import os
import sqlite3
import pandas as pd
from django.conf import settings

def get_df_from_sql(sql:str):
    # Execute query and get results as DataFrame
    db_path = os.path.join(settings.BASE_DIR, 'chinook.sqlite')
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df