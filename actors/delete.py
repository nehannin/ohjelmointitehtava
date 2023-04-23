import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor(prepared=True)

    # Pyydetään käyttäjältä sen näyttelijän ID kenet halutaan poistaa
    actor_id = input("Anna poistettavan näyttelijän ID: ")

    query = ("DELETE titles_has_actors FROM titles_has_actors JOIN actors ON actors.id = titles_has_actors.actors_id WHERE actors.id = %s;")
    cursor.execute(query, (actor_id,))
    query = ("DELETE FROM actors WHERE id = %s;")
    cursor.execute(query, (actor_id,))
    connection.commit()

    print("Näyttelijä on poistettu.")

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
