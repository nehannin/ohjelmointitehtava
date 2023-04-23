import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor(buffered=True)

    title_id = input("Anna sen nimikkeen ID mistä haluat poistaa arvostelun: ")

    query = ("SELECT id, name, year, duration FROM titles WHERE id = %s;")
    cursor.execute(query, (title_id,))
    title = cursor.fetchone()

    if title is not None:
        # Tulostetaan nimikkeen tiedot
        print(f"ID: {title[0]} NIMI: {title[1]} JULKAISUVUOSI: {title[2]} KESTO: {title[3]}")

        # Haetaan nimikkeen kaikki arvostelut
        query = ("SELECT id, review FROM reviews WHERE titles_id = %s")
        cursor.execute(query, (title_id,))
        reviews = cursor.fetchall()

        if len(reviews) > 0:
            # Tulostetaan kaikki arvostelut
            print("ARVOSTELUT:")
            for review in reviews:
                print(f"- ID: {review[0]} ARVOSTELU: {review[1]}")

            # Pyydetään käyttäjää syöttämään sen arvostelun ID jonka haluaa poistaa
            review_id = input("Anna sen arvostelun ID, jonka haluat poistaa: ")

            delete_review_query = ("DELETE FROM reviews WHERE id = %s AND titles_id = %s;")
            cursor.execute(delete_review_query, (review_id, title_id))
            if cursor.rowcount == 0:
                raise ValueError("Arvostelua ei löytynyt.")

            connection.commit()
            print("Arvostelu on poistettu.")
        else:
            print("Tällä nimikkeellä ei ole arvosteluja.")
    else:
        print("Nimikettä ei löydy.")

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
