#!/usr/bin/env python3
# Usage: importcsv.py datafile.csv scala_table_name
import os, sys
import pandas as pd
from sqlalchemy import create_engine
pguser='postgres'
pgpass='pgscala'
csvfile=sys.argv[1]
tablename=sys.argv[2]
schemaname="public"
df = pd.read_csv(csvfile)
engine = create_engine(f"postgresql://{pguser}:{pgpass}@localhost:5432/scala")
df.to_sql(tablename, engine, schema=schemaname, if_exists="fail", index=False)
