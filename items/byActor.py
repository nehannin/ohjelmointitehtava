import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor()

    # Pyydetään käyttäjältä sen näyttelijän ID kenen nimikkeet halutaan nähdä
    actor_id = input("Näyttelijän ID: ")

    query = ("SELECT "
             "actors.first_name, actors.last_name, "
             "titles.name, titles.year, titles.duration, "
             "description.description, "
             "title_types.type, "
             "categories.name "
             "FROM titles "
             "LEFT JOIN titles_has_actors ON titles.id = titles_has_actors.titles_id "
             "LEFT JOIN actors ON actors.id = titles_has_actors.actors_id "
             "LEFT JOIN description ON description.id = titles.description_id "
             "LEFT JOIN titles_has_title_types ON titles.id = titles_has_title_types.titles_id "
             "LEFT JOIN title_types ON title_types.id = titles_has_title_types.title_types_id "
             "LEFT JOIN categories_has_titles ON categories_has_titles.titles_id = titles.id "
             "LEFT JOIN categories ON categories.id = categories_has_titles.categories_id "
             "WHERE actors.id = %s;")
    cursor.execute(query, (actor_id,))
    results = cursor.fetchall()

    if results:
        print(f"Näyttelijän {actor_id} roolit seuraavissa nimikkeissä:")
        for result in results:
            print(f"{result[0]} {result[1]}: {result[2]} ({result[3]}), kesto: {result[4]}, kuvaus: {result[5]}, tyyppi: {result[6]}, kategoria: {result[7]}")
    else:
        print("Näyttelijää ei löydy rooleista!")

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
