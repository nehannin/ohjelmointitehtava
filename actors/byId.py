import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor(prepared=True)

    # Pyydetään käyttäjältä halutun näyttelijän ID:tä
    actor_id = input("Anna näyttelijän ID: ")

    query = ("SELECT actors.first_name, actors.last_name, actors.date_of_birth,titles.name, titles.year, titles.duration,description.description,title_types.type,categories.name,recommendation.age_limit FROM actors LEFT JOIN titles_has_actors ON actors.id = titles_has_actors.actors_id LEFT JOIN titles ON titles_has_actors.titles_id = titles.id LEFT JOIN titles_has_title_types ON titles.id = titles_has_title_types.titles_id LEFT JOIN title_types ON titles_has_title_types.title_types_id = title_types.id LEFT JOIN description ON titles.description_id = description.id LEFT JOIN categories_has_titles ON titles.id = categories_has_titles.titles_id LEFT JOIN categories ON categories_has_titles.categories_id = categories.id LEFT JOIN recommendation ON recommendation.id = titles.recommendation_id WHERE actors.id = %s;")
    cursor.execute(query, (actor_id,))
    results = cursor.fetchall()

    # Jos ID:tä vastaan löytyy näyttelijä, tulostetaan tämän tiedot
    if results:
        print(f"Näyttelijä: {results[0][0]} {results[0][1]} ({results[0][2]})")
        print("\nNimikkeet:")
        for result in results:
            print(f"- {result[3]} ({result[4]}), kesto: {result[5]}")
            print(f"  Kuvaus: {result[6]}")
            print(f"  Tyyppi: {result[7]}")
            print(f"  Kategoria: {result[8]}")
            print(f"  Ikäraja: {result[9]}")

    # Jos ID:tä vastaan ei löydy näyttelijää, ilmoitetaan siitä käyttäjälle
    else:
        print("Näyttelijää ei löydy tai hän ei ole mukana yhdessäkään nimikkeessä.")

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
