import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor(prepared=True)
    cursor = connection.cursor(buffered=True)

    connection.autocommit = False

    # Pyydetään käyttäjältä nimikkeen tiedot
    title_name = input("Nimi: ")
    title_year = input("Julkaisuvuosi: ")
    title_duration = input("Kesto: ")
    description_text = input("Kuvaus: ")
    recommendation = input("Ikärajasuositus: ")
    category = input("Kategoria: ")
    title_type = input("Tyyppi (elokuva/kirja/äänikirja): ")

    # Lisätään data description pöytään
    description_query = ("INSERT INTO description (description) VALUES (%s);")
    description_data = (description_text,)
    cursor.execute(description_query, description_data)
    description_id = cursor.lastrowid

    # Lisätään data recommendation pöytään
    recommendation_query = ("INSERT INTO recommendation (age_limit) VALUES (%s);")
    recommendation_data = (recommendation,)
    cursor.execute(recommendation_query, recommendation_data)
    recommendation_id = cursor.lastrowid

    # Lisätään data categories pöytään
    category_query = ("INSERT INTO categories (name) VALUES (%s);")
    category_data = (category,)
    cursor.execute(category_query, category_data)
    category_id = cursor.lastrowid

    # Lisätään data title_types pöytään
    type_query = ("INSERT INTO title_types (type) VALUES (%s);")
    type_data = (title_type,)
    cursor.execute(type_query, type_data)
    type_id = cursor.lastrowid

    # Lisätään data titles pöytään
    title_query = ("INSERT INTO titles (name, year, duration, description_id, recommendation_id) VALUES (%s, %s, %s, %s, %s);")
    title_data = (title_name, title_year, title_duration, description_id, recommendation_id)
    cursor.execute(title_query, title_data)
    title_id = cursor.lastrowid

    # Otetaan oikea ID categories pöydästä
    category_id_query = ("SELECT id FROM categories WHERE name = (%s);")
    category_id_data = (category,)
    cursor.execute(category_id_query, category_id_data)
    category_result = cursor.fetchone()
    if category_result is None:
        raise ValueError("Kategoriaa ei löydy!")
    category_id = category_result[0]

    categories_has_titles_query = ("INSERT INTO categories_has_titles (titles_id, categories_id) VALUES (%s, %s);")
    categories_has_titles_data = (title_id, category_id)
    cursor.execute(categories_has_titles_query, categories_has_titles_data)
    cursor.fetchone()

    # Otetaan oikea ID title_types pöydästä
    type_id_query = ("SELECT id FROM title_types WHERE type = (%s);")
    type_id_data = (title_type,)
    cursor.execute(type_id_query, type_id_data)
    type_result = cursor.fetchone()
    if type_result is None:
        raise ValueError("Tyyppiä ei löydy!")
    type_id = type_result[0]

    titles_has_title_types_query = ("INSERT INTO titles_has_title_types (titles_id, title_types_id) VALUES (%s, %s);")
    titles_has_title_types_data = (title_id, type_id)
    cursor.execute(titles_has_title_types_query, titles_has_title_types_data)
    cursor.fetchone()

    connection.commit()
    print("Tiedot lisätty onnistuneesti!")

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
