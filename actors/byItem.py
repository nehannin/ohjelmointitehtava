import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor()

    # Pyydetään käyttäjältä sen nimikkeen ID minkä näyttelijät halutaan saada
    title_id = input("Nimikkeen ID: ")

    title_query = ("SELECT "
                   "titles.name, titles.year, titles.duration, "
                   "description.description, title_types.type, categories.name "
                   "FROM titles "
                   "LEFT JOIN description ON description.id = titles.description_id "
                   "LEFT JOIN titles_has_title_types ON titles.id = titles_has_title_types.titles_id "
                   "LEFT JOIN title_types ON title_types.id = titles_has_title_types.title_types_id "
                   "LEFT JOIN categories_has_titles ON categories_has_titles.titles_id = titles.id "
                   "LEFT JOIN categories ON categories.id = categories_has_titles.categories_id "
                   "WHERE titles.id = %s;")

    cursor.execute(title_query, (title_id,))
    title_result = cursor.fetchone()

    if title_result:
        print(f"Nimikkeen tiedot: {title_result[0]} ({title_result[1]}), kesto: {title_result[2]}")
        print(f"Kuvaus: {title_result[3]}")
        print(f"Tyyppi: {title_result[4]}")
        print(f"Kategoria: {title_result[5]}\n")

        # Haetaan kaikki näyttelijät käyttäjän syöttämällä nimikkeen ID:llä
        actors_query = ("SELECT actors.first_name, actors.last_name "
                        "FROM actors "
                        "LEFT JOIN titles_has_actors ON actors.id = titles_has_actors.actors_id "
                        "WHERE titles_has_actors.titles_id = %s;")

        cursor.execute(actors_query, (title_id,))
        actors_results = cursor.fetchall()

        if actors_results:
            print("Näyttelijät:")
            for actor in actors_results:
                print(f"{actor[0]} {actor[1]}")
        else:
            print("Nimikkeessä ei ole näyttelijöitä!")
    else:
        print("Nimikettä ei löydy!")

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
