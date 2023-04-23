import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor(prepared=True)

    query = ("SELECT "
             "titles.id, titles.name, titles.year, titles.duration, "
             "description.id, description.description, "
             "recommendation.id, recommendation.age_limit, "
             "categories.id, categories.name, "
             "title_types.id, title_types.type "
             "FROM titles "
             "LEFT JOIN description ON description.id = titles.description_id "
             "LEFT JOIN recommendation ON recommendation.id = titles.recommendation_id "
             "LEFT JOIN categories_has_titles ON titles.id = categories_has_titles.titles_id "
             "LEFT JOIN categories ON categories.id = categories_has_titles.categories_id "
             "LEFT JOIN titles_has_title_types ON titles.id = titles_has_title_types.titles_id "
             "LEFT JOIN title_types ON title_types.id = titles_has_title_types.title_types_id;")
    cursor.execute(query)

    # Tulostetaan kaikki nimikkeet ja niiden tiedot
    for (titles_id, name, year, duration, description_id, description, recommendation_id, age_limit, categories_id, categories_name, title_types_id, title_types_type) in cursor:
        print(f"ID: {titles_id} NIMI: {name} JULKAISUVUOSI: {year} KESTO: {duration} min KUVAUS: {description} IKÄRAJASUOSITUS: {age_limit} KATEGORIA: {categories_name} TYYPPI: {title_types_type}")

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
