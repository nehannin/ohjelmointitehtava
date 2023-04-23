import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor(prepared=True)
    cursor = connection.cursor(buffered=True)
    connection.autocommit = False

    # Pyydetään käyttäjältä sen nimikkeen ID mihin haluaa lisätä arvostelun
    title_id = input("Arvioitavan nimikkeen ID: ")

    get_query = ("SELECT "
                 "reviews.id, reviews.review, "
                 "titles.id, titles.name, titles.year, titles.duration, titles.description_id, titles.recommendation_id "
                 "FROM reviews "
                 "RIGHT JOIN titles ON titles.id = reviews.titles_id "
                 "WHERE titles.id = (%s);")
    cursor.execute(get_query, (title_id,))

    result = cursor.fetchone()

    if result:
        (current_review_id, current_review, current_title_id, current_name, current_year, current_duration, current_description_id, current_recommendation_id) = result

        review_text = input("Anna arvostelu: ")
        new_name = ""
        new_year = ""
        new_duration = ""

        if new_name.strip() == "":
            new_name = current_name

        if new_year.strip() == "":
            new_year = current_year

        if new_duration.strip() == "":
            new_duration = current_duration

        update_query = "UPDATE titles SET name=%s, year=%s, duration=%s WHERE id=%s"
        update_data = (new_name, new_year, new_duration, title_id)
        cursor.execute(update_query, update_data)

    else:
        current_review_id = None
        current_review = None

        current_name = input("Anna nimike: ")
        current_year = input("Anna vuosi: ")
        current_duration = input("Anna kesto: ")
        current_description_id = None
        current_recommendation_id = None

        # Lisätään data titles pöytään
        title_query = "INSERT INTO titles (id, name, year, duration, description_id, recommendation_id) VALUES (%s, %s, %s, %s, %s, %s)"
        title_data = (title_id, current_name, current_year, current_duration, current_description_id, current_recommendation_id)
        cursor.execute(title_query, title_data)
        title_id = cursor.lastrowid

        review_text = input("Anna arviointi: ")

    # Lisätään data reviews pöytään
    review_query = "INSERT INTO reviews (titles_id, review) VALUES (%s, %s)"
    review_data = (title_id, review_text)
    cursor.execute(review_query, review_data)
    reviews_id = cursor.lastrowid

    connection.commit()
    print("Arvostelu lisätty onnistuneesti!")

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()
