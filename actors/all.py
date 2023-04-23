import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor(prepared=True)

    # Haetaan kaikkien näyttelijöiden tiedot actors -taulusta
    query = ("SELECT * FROM actors;")
    cursor.execute(query)

    actors = cursor.fetchall()

    for (id, first_name, last_name, date_of_birth) in actors:
        print(f"{id} {first_name} {last_name} {date_of_birth}")

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
