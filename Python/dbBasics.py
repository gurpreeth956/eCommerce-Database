import pymysql


def insert():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Person(ID, Email, Named, DateOfBirth, Phone, Address, DateJoined, IsEmployee)\
                values(\"11111\", \"111.sanjr@gmail.com\", \"BILL\", \"1912-02-07\", \"4545454545\", \"Hurst\",\
                \"2015-05-15\", \"N\")"
        cursor.execute(query)
        client.commit()
    except Exception:
        print(Exception)
        client.rollback()
    finally:
        client.close()


def select():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT ID, Email, Named, DateOfBirth, Phone, Address, DateJoined, IsEmployee FROM Person"
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            idnum = row[0]
            named = row[2]
            print("ID: {} NAME: {}".format(idnum, named))
    finally:
        client.close()


# To test methods:
# insert()
# select()
