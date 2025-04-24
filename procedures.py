import psycopg2
from tabulate import tabulate

conn = psycopg2.connect(
    host='localhost',
    dbname='phonebook',
    user='aio',
    password='',
    port=5432
)
cur = conn.cursor()

print("""
Procedure Menu:
1. 's' - Search by pattern (name, surname, phone)
2. 'i' - Insert or update one user
3. 'm' - Insert many users (with validation)
4. 'p' - Paginate data (limit + offset)
5. 'd' - Delete by name + surname or phone number
6. 'f' - Exit
""")

while True:
    command = input("Enter procedure: ").lower()

    if command == 's':
        pattern = input("Enter search pattern: ")
        cur.execute("SELECT * FROM search_phonebook(%s);", (pattern,))
        rows = cur.fetchall()
        print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt="fancy_grid"))

    elif command == 'i':
        name = input("Name: ")
        surname = input("Surname: ")
        phone = input("Phone: ")
        cur.execute("CALL insert_or_update_user(%s, %s, %s);", (name, surname, phone))
        conn.commit()
        print("User inserted or updated.")

    elif command == 'm' :
        count = int(input("How many users to insert? "))
        names, surnames, phones = [], [], []
        for i in range(count) :
            print(f"User #{i+1}")
            names.append(input("Name: "))
            surnames.append(input("Surname: "))
            phones.append(input("Phone: "))

        cur.execute("CALL insert_many_users(%s, %s, %s);", (names, surnames, phones))
        conn.commit()
        print("Users inserted (or updated). Invalid entries, if any, are shown in PostgreSQL NOTICE.")

    elif command == 'p' :
        limit = int(input("Limit: "))
        offset = int(input("Offset: "))
        cur.execute("SELECT * FROM get_phonebook_page(%s, %s);", (limit, offset))
        rows = cur.fetchall()
        print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt="fancy_grid"))

    elif command == 'd':
        name = input("Name (optional): ").strip()
        surname = input("Surname (optional): ").strip()
        phone = input("Phone (optional): ").strip()
        cur.execute("CALL delete_user_by_name_or_phone(%s, %s, %s);", (name, surname, phone))
        conn.commit()
        print("Deletion completed.")

    elif command == 'f':
        print("Bye!")
        break

cur.close()
conn.close()

