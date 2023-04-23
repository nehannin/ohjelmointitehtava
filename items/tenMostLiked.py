import mysql.connector

# Yhdistetään tietokanta
connection = None
cursor = None

try:
    connection = mysql.connector.connect(database='suunnittelutehtava3', user='root')
    cursor = connection.cursor(prepared=True)

    query = ("SELECT titles.id, titles.name, "
             "AVG(reviews.review) AS avg_review "
             "FROM titles "
             "LEFT JOIN reviews ON reviews.titles_id = titles.id "
             "GROUP BY titles.id "
             "ORDER BY avg_review "
             "DESC LIMIT 10;")
    cursor.execute(query)
    titles = cursor.fetchall()

    # Tulostetaan 10 suosituinta nimikettä arvostelujen keskiarvon perusteella
    if len(titles) > 0:
        print("10 suosituinta nimikettä:")
        for index, (titles_id, name, avg_review) in enumerate(titles, 1):
            print(f"{index}. ID: {titles_id} NIMI: {name} KESKIARVO: {avg_review:.2f}")
    else:
        print("Ei nimikkeitä.")

except Exception as e:
    print(e)

finally:
    # Suljetaan yhteys
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
