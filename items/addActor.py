import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor(prepared=True)
    connection.autocommit = False

    # Pyydetään käyttäjältä nimikkeen ID mihin haluaa lisätä näyttelijän
    title_id = input("Anna nimikkeen ID mihin haluat lisätä näyttelijän: ")

    # Pyydetään käyttäjältä näyttelijän ID jonka haluaa lisätä nimikkeeseen
    actor_id = input("Anna näyttelijän ID: ")

    # Tarkistetaan löytyykö title ID tietokannasta
    title_query = ("SELECT id FROM titles WHERE id = %s;")
    title_data = (title_id,)
    cursor.execute(title_query, title_data)
    title_result = cursor.fetchone()

    if not title_result:
        print("Nimikettä ei löytynyt!")
        exit()

    # Tarkistetaan löytyykö näyttelijän ID tietokannasta
    actor_query = ("SELECT id FROM actors WHERE id = %s;")
    actor_data = (actor_id,)
    cursor.execute(actor_query, actor_data)
    actor_result = cursor.fetchone()

    if not actor_result:
        print("Näyttelijää ei löytynyt!")
        exit()

    titles_actors_query = ("INSERT INTO titles_has_actors (titles_id, actors_id) VALUES (%s, %s);")
    titles_actors_data = (title_id, actor_id)
    cursor.execute(titles_actors_query, titles_actors_data)

    connection.commit()
    print("Näyttelijä lisätty nimikkeeseen onnistuneesti!")

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()
