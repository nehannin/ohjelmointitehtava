import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor(prepared=True)
    cursor = connection.cursor(buffered=True)

    title_id = input("Anna päivitettävän nimikkeen ID: ")

    query = ("SELECT "
             "titles.id, titles.name, titles.year, titles.duration, "
             "description.description, "
             "recommendation.age_limit, "
             "title_types.type, "
             "categories.name "
             "FROM titles "
             "LEFT JOIN description ON description.id = titles.description_id "
             "LEFT JOIN recommendation ON recommendation.id = titles.recommendation_id "
             "LEFT JOIN titles_has_title_types ON titles.id = titles_has_title_types.titles_id "
             "LEFT JOIN title_types ON title_types.id = titles_has_title_types.title_types_id "
             "LEFT JOIN categories_has_titles ON categories_has_titles.titles_id = titles.id "
             "LEFT JOIN categories ON categories.id = categories_has_titles.categories_id "
             "WHERE titles.id = %s;")
    cursor.execute(query, (title_id, ))
    (current_id, current_name, current_year, current_duration, current_description, current_recommendation, current_type, current_category) = cursor.fetchone()

    # Pyydetään käyttäjältä nimikkeen uudet tiedot
    new_name = input("Uusi nimi: ")
    new_year = input("Uusi julkaisuvuosi: ")
    new_duration = input("Uusi kesto: ")
    new_description = input("Uusi kuvaus: ")
    new_recommendation = input("Uusi ikärajasuositus: ")
    new_type = input("Uusi tyyppi (elokuva/kirja/äänikirja): ")
    new_category = input("Uusi kategoria: ")

    if new_name.strip() == "":
        new_name = current_name

    if new_year.strip() == "":
        new_year = current_year

    if new_duration.strip() == "":
        new_duration = current_duration

    if new_description.strip() == "":
        new_description = current_description

    if new_recommendation.strip() == "":
        new_recommendation = current_recommendation

    if new_type.strip() == "":
        new_type = current_type

    if new_category.strip() == "":
        new_category = current_category

    update_query = ("UPDATE titles "
                    "LEFT JOIN description ON description.id = titles.description_id "
                    "LEFT JOIN recommendation ON recommendation.id = titles.recommendation_id "
                    "LEFT JOIN titles_has_title_types ON titles.id = titles_has_title_types.titles_id "
                    "LEFT JOIN title_types ON title_types.id = titles_has_title_types.title_types_id "
                    "LEFT JOIN categories_has_titles ON categories_has_titles.titles_id = titles.id "
                    "LEFT JOIN categories ON categories.id = categories_has_titles.categories_id "
                    "SET "
                    "titles.name = %s, "
                    "titles.year = %s, "
                    "titles.duration = %s, "
                    "description.description = %s, "
                    "recommendation.age_limit = %s, "
                    "title_types.type = %s, "
                    "categories.name = %s "
                    "WHERE titles.id = %s;")
    cursor.execute(update_query, (new_name, new_year, new_duration, new_description, new_recommendation, new_type, new_category, title_id))
    connection.commit()

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
