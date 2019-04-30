import pymysql


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


'''
BELOW ARE ALL THE METHODS FOR GETTING AND SETTING FROM THE DATABASE.

NOTE: THIS FILE IS TEMPORARY AND THE METHODS WILL BE MOVED TO THE NECESSARY FILE(S) WHEN THEY ARE CREATED
'''


# Person Table
def insertPerson(idvar, email, name, birthdate, phone, address, datejoined, isemployee, username, userpass,
                 hasmembership, employeeid, supervisor):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Person(ID, Email, Named, DateOfBirth, Phone, Address, DateJoined, IsEmployee)\
            values(%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (idvar, email, name, birthdate, phone, address, datejoined, isemployee))
        client.commit()

        if isEmployeeVar == 'N':
            insertCustomer(idVar, username, userpass, hasmembership)
        elif isEmployeeVar == 'Y':
            insertEmployee(idVar, employeeid, supervisor)
    except Exception:
        print("Could not add entity to Person Table")
        client.rollback()
    finally:
        client.close()


def getPersonTuple(idvar):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT ID, Email, Named, DateOfBirth, Phone, Address, DateJoined, IsEmployee FROM Person WHERE ID = %s"
        cursor.execute(query, idvar)
        result = cursor.fetchall()
        return result
    except Exception:
        print("Could not retrieve specified Person Entity")
    finally:
        client.close()


def getPersonTable():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT ID, Email, Named, DateOfBirth, Phone, Address, DateJoined, IsEmployee FROM Person"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve Person Table data")
    finally:
        client.close()


# Customer Table
def insertCustomer(idvar, username, userpass, hasmembership):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Customer(ID, Username, Userpass, HasMembership) values(%s, %s, %s, %s)"
        cursor.execute(query, (idvar, username, userpass, hasmembership))
        client.commit()
    except Exception:
        print("Could not add entity to Customer Table")
        client.rollback()
    finally:
        client.close()


def getCustomerTuple(idvar):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT ID, Username, Userpass, HasMembership FROM Customer WHERE ID = %s"
        cursor.execute(query, idvar)
        result = cursor.fetchall()
        return result
    except Exception:
        print("Could not retrieve specified Customer Entity")
    finally:
        client.close()


def getCustomerTable():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT ID, Username, Userpass, HasMembership FROM Customer"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve Customer Table data")
    finally:
        client.close()


# Employee Table
def insertEmployee(idvar, employeeid, supervisor):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Employee(ID, EmployeeID, Supervisor) values(%s, %s, %s)"
        cursor.execute(query, (idvar, employeeid, supervisor))
        client.commit()
    except Exception:
        print("Could not add entity to Employee Table")
        client.rollback()
    finally:
        client.close()


def getEmployeeTuple(employeeid):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT ID, EmployeeID, Supervisor FROM Employee WHERE EmployeeID = %s"
        cursor.execute(query, employeeid)
        result = cursor.fetchall()
        return result
    except Exception:
        print("Could not retrieve specified Employee Entity")
    finally:
        client.close()


def getEmployeeTable():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT ID, EmployeeID, Supervisor FROM Employee"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve Employee Table data")
    finally:
        client.close()


# Item Table
def insertItem(itemid, quantity, price, itemtype, seller, itemdesc, category, url):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Item(ItemID, Quantity, Price, ItemType, Seller, ItemDesc, Category, URL) \
            values(%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (itemid, quantity, price, itemtype, seller, itemdesc, category, url))
        client.commit()
    except Exception:
        print("Could not add entity to Item Table")
        client.rollback()
    finally:
        client.close()


def getItemTuple(itemid):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT ItemID, Quantity, Price, ItemType, Seller, ItemDesc, Category, URL FROM Item WHERE ItemID = %s"
        cursor.execute(query, itemid)
        result = cursor.fetchall()
        return result
    except Exception:
        print("Could not retrieve specified Item Entity")
    finally:
        client.close()


def getItemTable():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT ItemID, Quantity, Price, ItemType, Seller, ItemDesc, Category, URL FROM Item"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve Item Table data")
    finally:
        client.close()


# ShoppingCart Table
def insertShoppingCart(customerid, itemid, quantity):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO ShoppingCart(CustomerID, ItemID, Quantity) values(%s, %s, %s)"
        cursor.execute(query, (customerid, itemid, quantity))
        client.commit()
    except Exception:
        print("Could not add entity to ShoppingCart Table")
        client.rollback()
    finally:
        client.close()


def getShoppingCartTuple(customerid, itemid):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT CustomerID, ItemID, Quantity FROM Customer WHERE CustomerID = %s AND ItemID = %s"
        cursor.execute(query, (customerid, itemid))
        result = cursor.fetchall()
        return result
    except Exception:
        print("Could not retrieve specified ShoppingCart Entity")
    finally:
        client.close()


def getShoppingCartTable():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT CustomerID, ItemID, Quantity FROM Customer"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve ShoppingCart Table data")
    finally:
        client.close()


# WishList Table
def insertWishList(customerid, itemid):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO WishList(CustomerID, ItemID) values(%s, %s, %s)"
        cursor.execute(query, (customerid, itemid))
        client.commit()
    except Exception:
        print("Could not add entity to WishList Table")
        client.rollback()
    finally:
        client.close()


def getWishListTuple(customerid, itemid):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT CustomerID, ItemID FROM WishList WHERE CustomerID = %s AND ItemID = %s"
        cursor.execute(query, (customerid, itemid))
        result = cursor.fetchall()
        return result
    except Exception:
        print("Could not retrieve specified WishList Entity")
    finally:
        client.close()


def getWishListTable():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT CustomerID, ItemID FROM WishList"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve WishList Table data")
    finally:
        client.close()


# Discount Table
def insertDiscount(discountid, discountprice, excdate):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Discount(DiscountID, DiscountPrice, ExpDate) values(%s, %s, %s)"
        cursor.execute(query, (discountid, discountprice, excdate))
        client.commit()
    except Exception:
        print("Could not add entity to Discount Table")
        client.rollback()
    finally:
        client.close()


def getDiscountTuple(discountid):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT DiscountID, DiscountPrice, ExpDate FROM Discount WHERE DiscountID = %s"
        cursor.execute(query, discountid)
        result = cursor.fetchall()
        return result
    except Exception:
        print("Could not retrieve specified Discount Entity")
    finally:
        client.close()


def getDiscountTable():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT DiscountID, DiscountPrice, ExpDate"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve Discount Table data")
    finally:
        client.close()


# Orders Table
def insertOrders(orderid, customerid, orderdate, completed, discountid):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Item(OrderNum, CustomerID, OrderDate, Completed, DiscountID) values(%s, %s, %s, %s, %s)"
        cursor.execute(query, (orderid, customerid, orderdate, completed, discountid))
        client.commit()
    except Exception:
        print("Could not add entity to Orders Table")
        client.rollback()
    finally:
        client.close()


def getOrdersTuple(orderid):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT OrderNum, CustomerID, OrderDate, Completed, DiscountID FROM Orders WHERE OrderNum = %s"
        cursor.execute(query, orderid)
        result = cursor.fetchall()
        return result
    except Exception:
        print("Could not retrieve specified Orders Entity")
    finally:
        client.close()


def getOrdersTable():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT OrderNum, CustomerID, OrderDate, Completed, DiscountID"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve Orders Table data")
    finally:
        client.close()


# OrderedItems Table
def insertOrderedItems(orderid, itemid, quantity):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO OrderedItems(OrderID, ItemID, Quantity) values(%s, %s, %s)"
        cursor.execute(query, (orderid, itemid, quantity))
        client.commit()
    except Exception:
        print("Could not add entity to OrderedItems Table")
        client.rollback()
    finally:
        client.close()


def getOrderedItemsTuple(orderid, itemid):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT OrderID, ItemID, Quantity FROM OrderedItems WHERE OrderID = %s AND ItemID = %s"
        cursor.execute(query, (orderid, itemid))
        result = cursor.fetchall()
        return result
    except Exception:
        print("Could not retrieve specified OrderedItems Entity")
    finally:
        client.close()


def getOrderedItemsTable():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT OrderID, ItemID, Quantity FROM OrderedItems"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve specified OrderedItems Table data")
    finally:
        client.close()


# Payment Table
def insertPayment(orderid, cardnum, cvs, cardcomp, cardtype, cardexp):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Payment(OrderID, CardNum, CVS, CardComp, CardType, CardExp) values(%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (orderid, cardnum, cvs, cardcomp, cardtype, cardexp))
        client.commit()
    except Exception:
        print("Could not add entity to Payment Table")
        client.rollback()
    finally:
        client.close()


def getPaymentTuple(orderid):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT OrderID, CardNum, CVS, CardComp, CardType, CardExp FROM Payment WHERE OrderID = %s"
        cursor.execute(query, orderid)
        result = cursor.fetchall()
        return result
    except Exception:
        print("Could not retrieve specified Payment Entity")
    finally:
        client.close()


def getPaymentTable():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT OrderID, CardNum, CVS, CardComp, CardType, CardExp"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve Payment Table data")
    finally:
        client.close()


# Shipment Table
def insertShipment(orderid, address, details, fee, company):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Shipment(OrderID, Address, Details, Fee, Company) values(%s, %s, %s, %s, %s)"
        cursor.execute(query, (orderid, address, details, fee, company))
        client.commit()
    except Exception:
        print("Could not add entity to Shipment Table")
        client.rollback()
    finally:
        client.close()


def getShipmentTuple(orderid):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT OrderID, Address, Details, Fee, Company FROM Shipment WHERE OrderID = %s"
        cursor.execute(query, orderid)
        result = cursor.fetchall()
        return result
    except Exception:
        print("Could not retrieve specified Shipment Entity")
    finally:
        client.close()


def getShipmentTable():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT OrderID, Address, Details, Fee, Company"
        cursor.execute(query, orderid)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve Shipment Table data")
    finally:
        client.close()


# Returnment Table
def insertReturnment(orderid, itemid, quantity, comments):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Returnment(OrderID, ItemID, Quantity, Comments) values(%s, %s, %s, %s)"
        cursor.execute(query, (orderid, itemid, quantity, comments))
        client.commit()
    except Exception:
        print("Could not add entity to Returnment Table")
        client.rollback()
    finally:
        client.close()


def getReturnmentTuple(orderid, itemid, quantity):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT OrderID, ItemID, Quantity, Comments FROM Returnment WHERE OrderID = %s AND ItemID = %s \
            AND Quantity = %s"
        cursor.execute(query, (orderid, itemid, quantity))
        result = cursor.fetchall()
        return result
    except Exception:
        print("Could not retrieve specified Returnment Entity")
    finally:
        client.close()


def getReturnmentTable():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT OrderID, ItemID, Quantity, Comments FROM Returnment"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve Returnment Table data")
    finally:
        client.close()


# Reviews Table
def insertReview(customerid, itemid, ratings, comments):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Reviews(CustomerID, ItemID, Ratings, Comments) values(%s, %s, %s, %s)"
        cursor.execute(query, (customerid, itemid, ratings, comments))
        client.commit()
    except Exception:
        print("Could not add entity to Reviews Table")
        client.rollback()
    finally:
        client.close()


def getReviewTuple(customerid, itemid):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT CustomerID, ItemID, Ratings, Comments FROM Reviews WHERE CusotmerID = %s AND ItemID = %s"
        cursor.execute(query, (customerid, itemid))
        result = cursor.fetchall()
        return result
    except Exception:
        print("Could not retrieve specified Reviews Entity")
    finally:
        client.close()


def getReviewTable():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT CustomerID, ItemID, Ratings, Comments FROM Reviews"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve Reviews Table data")
    finally:
        client.close()
