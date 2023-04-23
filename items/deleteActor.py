import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor(prepared=True)
    connection.autocommit = False

    title_id = input("Anna nimikkeen ID josta haluat poistaa näyttelijän: ")

    # Tarkistetaan löytyykö käyttäjän syöttämän nimikkeen ID tietokannasta
    title_query = "SELECT id FROM titles WHERE id = %s"
    title_data = (title_id,)
    cursor.execute(title_query, title_data)
    title_result = cursor.fetchone()

    if not title_result:
        print("Nimikettä ei löytynyt!")
        exit()

    actor_id = input("Anna näyttelijän ID jonka haluat poistaa nimikkeestä: ")

    # Tarkistetaan löytyykö käyttäjän syöttämän näyttelijän ID tietokannasta
    actor_query = "SELECT id FROM actors WHERE id = %s"
    actor_data = (actor_id,)
    cursor.execute(actor_query, actor_data)
    actor_result = cursor.fetchone()

    if not actor_result:
        print("Näyttelijää ei löytynyt!")
        exit()

    title_actor_query = "SELECT * FROM titles_has_actors WHERE titles_id = %s AND actors_id = %s"
    title_actor_data = (title_id, actor_id)
    cursor.execute(title_actor_query, title_actor_data)
    title_actor_result = cursor.fetchone()

    if not title_actor_result:
        print("Näyttelijää ei löytynyt kyseisestä nimikkeestä!")
        exit()

    # Poistetaan näyttelijä valitusta nimikkeestä
    title_actor_delete_query = "DELETE FROM titles_has_actors WHERE titles_id = %s AND actors_id = %s"
    title_actor_delete_data = (title_id, actor_id)
    cursor.execute(title_actor_delete_query, title_actor_delete_data)

    connection.commit()
    print("Näyttelijä poistettu nimikkeestä onnistuneesti!")

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()
