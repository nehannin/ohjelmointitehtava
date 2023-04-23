import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor(prepared=True)

    # Pyydetään käyttäjältä näyttelijän tiedot
    first_name = input("Näyttelijän etunimi: ")
    last_name = input("Näyttelijän sukunimi: ")
    date_of_birth = input("Näyttelijän syntymävuosi: ")

    query = ("INSERT INTO actors(first_name, last_name, date_of_birth) VALUES((%s), (%s), (%s));")
    cursor.execute(query, (first_name, last_name, date_of_birth))
    connection.commit()

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
