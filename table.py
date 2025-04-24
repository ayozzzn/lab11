import psycopg2
from tabulate import tabulate

conn = psycopg2.connect(
    dbname='phonebook',
    user='aio',
    password='',
    host='localhost',
    port=5432
)
cur = conn.cursor()
cur.execute("SELECT * FROM phonebook;")
rows = cur.fetchall()
print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt="fancy_grid"))

cur.close()
conn.close()
