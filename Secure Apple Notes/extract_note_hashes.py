import sys
import sqlite3

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} NoteStore.sqlite")
        sys.exit(1)

    database = sys.argv[1]

    try:
        with sqlite3.connect(database) as db:
            cursor = db.cursor()

            query = """
            SELECT Z_PK, ZCRYPTOITERATIONCOUNT, ZCRYPTOSALT, ZCRYPTOWRAPPEDKEY
            FROM ZICCLOUDSYNCINGOBJECT
            WHERE ZISPASSWORDPROTECTED = 1
            """
            cursor.execute(query)

            for row in cursor.fetchall():
                z_pk, iteration_count, salt, wrapped_key = row
                salt_hex = salt.hex() if salt else ''
                key_hex = wrapped_key.hex() if wrapped_key else ''
                print(f"$ASN$*{z_pk}*{iteration_count}*{salt_hex}*{key_hex}")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()