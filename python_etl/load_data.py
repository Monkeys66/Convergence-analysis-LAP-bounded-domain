from pathlib import Path
from getpass import getpass
import pandas as pd
import numpy as np
import psycopg

script_path = Path(__file__).resolve()
script_directory = script_path.parent
project_root = script_directory.parent

data_path = (
    project_root
    / "data_generation"
    / "ellipse_convergence.csv"
)

data_file = pd.read_csv(data_path)

epsilons = data_file["epsilon"]
relative_errors = data_file["relative_error"]

records = list(zip(epsilons, relative_errors))

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="lap_convergence",
    user="postgres",
    password=getpass("Enter your PostgreSQL password: "),
) as conn:

    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO ellipse_convergence (
                epsilon, 
                relative_error
            )
            VALUES (%s, %s)
            """,
            records
            )

        row = cur.execute(
            "SELECT COUNT(*) FROM ellipse_convergence;"
        ).fetchone()

        print(f"Database rows: {row[0]}")




