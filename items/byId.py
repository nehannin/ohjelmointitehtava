import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor(prepared=True)

    # Pyydetään käyttäjältä sen nimikkeen ID jonka tiedot haluaa nähdä
    title_id = input("Nimikkeen ID: ")

    query = ("SELECT "
             "titles.id, titles.name, titles.year, titles.duration, "
             "description.description, "
             "recommendation.age_limit, "
             "title_types.type, "
             "categories.name, "
             "reviews.review "
             "FROM titles "
             "LEFT JOIN description ON description.id = titles.description_id "
             "LEFT JOIN recommendation ON recommendation.id = titles.recommendation_id "
             "LEFT JOIN titles_has_title_types ON titles_id = titles_has_title_types.titles_id "
             "LEFT JOIN title_types ON title_types.id = titles_has_title_types.title_types_id "
             "LEFT JOIN categories_has_titles ON categories_id = categories_has_titles.categories_id "
             "LEFT JOIN categories ON categories.id = categories_has_titles.categories_id "
             "RIGHT JOIN reviews ON reviews.titles_id = titles.id "
             "WHERE titles.id = (%s);")
    cursor.execute(query, (title_id,))
    title = cursor.fetchone()

    if title is not None:
        # Tulostetaan kaikki muut tiedot vain kerran
        print(f"ID: {title[0]} NIMI: {title[1]} JULKAISUVUOSI: {title[2]} KESTO: {title[3]} KUVAUS: {title[4]} IKÄRAJASUOSITUS: {title[5]} TYYPPI: {title[6]} KATEGORIA: {title[7]}")

        # Tulostetaan valitun nimikkeen kaikki arvostelut loopilla
        reviews = set()
        for row in cursor:
            reviews.add(row[8])

        if len(reviews) > 0:
            print("ARVOSTELUT:")
            for review in reviews:
                print(f"- {review}")

    else:
        print("Nimikettä ei löydy tai sillä ei ole arvosteluja!")

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
