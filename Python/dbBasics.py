import pymysql
from datetime import datetime
import time


def insert():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Person(ID, Email, Named, DateOfBirth, Phone, Address, DateJoined, IsEmployee)\
                values(%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (123, 'asdf@gmail.com', 'Te', '1998-11-25', 6072165029, 'Ithaca', '1998-11-25', 'N'))
        client.commit()
    except Exception:
        print(Exception)
        client.rollback()
    finally:
        client.close()
    print('done')


def select():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        idvar = 123
        cursor = client.cursor()
        query = "SELECT ID, Email, Named, DateOfBirth, Phone, Address, DateJoined, IsEmployee FROM Person \
                WHERE ID = %s"
        cursor.execute(query, idvar)
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

def insertOrders():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    #try:
    cursor = client.cursor()
    query = "SELECT Category FROM Item GROUP BY Category"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row[0])
    #except Exception:
     #   print("Could not add entity to Orders Table")
     #   client.rollback()
    #finally:
    client.close()


now = datetime.now()
insertOrders()