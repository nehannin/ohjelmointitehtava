import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor(prepared=True)

    # Pyydetään käyttäjältä sen näyttelijän ID kenen tietoja halutaan muokata
    actor_id = input("Näyttelijän ID: ")

    get_query = ("SELECT * FROM actors WHERE id = (%s);")
    cursor.execute(get_query, (actor_id,))
    (current_id, current_first_name, current_last_name, current_date_of_birth) = cursor.fetchone()

    # Pyydetään käyttäjältä uudet tiedot
    new_first_name = input("Uusi etunimi: ")
    new_last_name = input("Uusi sukunimi: ")
    new_date_of_birth = input("Uusi syntymävuosi: ")

    if new_first_name.strip() == "":
        new_first_name = current_first_name

    if new_last_name.strip() == "":
        new_last_name = current_last_name

    if new_date_of_birth.strip() == "":
        new_date_of_birth = current_date_of_birth

    update_query = ("UPDATE actors SET first_name = (%s), last_name = (%s), date_of_birth = (%s) WHERE id = (%s)")
    cursor.execute(update_query, (new_first_name, new_last_name, new_date_of_birth, actor_id))
    connection.commit()

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
