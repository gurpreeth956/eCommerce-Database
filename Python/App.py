from flask import Flask, render_template, request, redirect
import pymysql.cursors
import datetime
from datetime import datetime as dt


# Do hard refresh on web page if something does not loading
app = Flask(__name__)


# Variables (make global in method if you are writing to it)
loggedinid = None
loggedinname = None
lastorderid = None


@app.route("/")
def home():
    global loggedinid, loggedinname, lastorderid
    if 'logoff' in request.args:
        loggedinid = None
        loggedinname = None
        lastorderid = None
    return render_template('index.html', loggedin=loggedinname, title='Home', styles='album.css', bodyclass='bg-light')


@app.route("/signup.html", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        table = getPersonTable()
        idn = len(table) + 1
        name = request.form['firstName']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        insertPerson(idn, email, name, '1998-11-25', phone, 'Ithaca', dt.today().strftime('%Y-%m-%d'), 'N')
        insertCustomer(idn, password, 'N')
        return redirect('/signin.html')
    return render_template('signup.html', title='Sign Up',  styles='signin.css', bodyclass='text-center')


@app.route("/signin.html", methods=['GET', 'POST'])
def login():
    global loggedinid, loggedinname
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
        try:
            cursor = client.cursor()
            query = "SELECT P.Email, C.CustomerID, C.Userpass, P.Named FROM Customer C, Person P " \
                    "WHERE C.CustomerID = P.ID"
            cursor.execute(query)
            results = cursor.fetchall()
            for customer in results:
                if customer[0] == email and customer[2] == password:
                    loggedinid = customer[1]
                    loggedinname = customer[3]
                    break
            if loggedinid != None:
                return redirect('/')
        except Exception:
            print("Can not retrieve specified Customer Entity")
        finally:
            client.close()
    return render_template('signin.html', title='Log In', styles='signin.css', bodyclass='text-center')


@app.route("/checkout.html", methods=['GET', 'POST'])
def checkout():
    global loggedinid, lastorderid
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    ordersuccessful = False
    items = None
    quantity = 0
    total = 0
    discount = 0
    shipment = 5
    addbtn = True
    try:
        # For things on the right side of the checkout page
        cursor = client.cursor()
        query = "SELECT I.ItemType, S.Quantity, I.ItemDesc, I.Price, S.ItemID " \
                "FROM Item I, ShoppingCart S WHERE S.CustomerID = %s AND I.ItemID = S.ItemID"
        cursor.execute(query, loggedinid)
        items = cursor.fetchall()

        hasmembership = 'Y'
        query = "SELECT HasMembership FROM Customer WHERE CustomerID = %s AND HasMembership = %s"
        cursor.execute(query, (loggedinid, hasmembership))
        currentcust = cursor.fetchall()

        # Get discounts and no shipping fee if member
        ismember = False
        for row in currentcust:
            ismember = True

        if ismember:
            valid = 'Y'
            query = "SELECT DiscountPercent FROM Discount WHERE Valid = %s"
            cursor.execute(query, valid)
            discountvalues = cursor.fetchall()
            for row in discountvalues:
                discount += row[0]
            shipment = 0

        # Get sum of prices
        for row in items:
            total += row[1] * row[3]
            quantity += row[1]

        total -= (total * discount)
        total += shipment
    except Exception:
        print('Could not get shopping cart data')
    finally:
        client.close()

    if request.method == 'POST':
        if 'checkout' in request.form:
            name = request.form['firstName'] + ' ' + request.form['secondName']
            email = request.form['email']
            billaddress = request.form['address'] + ' ' + request.form['address2'] + ' ' + request.form['state'] + ' ' + request.form['country'] + ' ' + request.form['zip']
            cardName = request.form['cardName']
            cardNum = request.form['cardNum']
            cardExp = request.form['expiration']
            cardCVV = request.form['cardCVV']
            cardType = request.form['cardType']
            shipname = request.form['firstNameShip'] + ' ' + request.form['secondNameShip']
            shipaddress = request.form['addressShip'] + ' ' + request.form['address2Ship'] + ' ' + request.form['stateShip'] + ' ' + request.form['countryShip'] + ' ' + request.form['zipShip']

            client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
            try:
                cursor = client.cursor()
                query = "SELECT CustomerID, ItemID, Quantity FROM ShoppingCart WHERE CustomerID = %s"
                cursor.execute(query, loggedinid)
                results = cursor.fetchall()

                # Create Orders Entity
                table = getOrdersTable()
                orderid = len(table) + 1
                query = "INSERT INTO Orders(OrderNum, CustomerID, OrderDate, Completed, DiscountID, OrderName, OrderEmail) \
                                values(%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (orderid, loggedinid, dt.today().strftime('%Y-%m-%d'), 'N', None, name, email)) # MAKE PENDING PAGE FOR ORDERS

                # Create Shipment Entity
                customer = getCustomerTuple(loggedinid)
                fee = '5'
                for row in customer:
                    if row[2] == 'Y':
                        fee = '0'
                query = "INSERT INTO Shipment(OrderID, Address, Fee, Company, ShipName) values(%s, %s, %s, %s, %s)"
                cursor.execute(query, (orderid, shipaddress, fee, 'UPS', shipname))

                # Create Payment Entity
                query = "INSERT INTO Payment(OrderID, CardName, CardNum, CardComp, CardExp, Billing) \
                        values(%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (orderid, cardName, cardNum, cardType, datetime.datetime.strptime('01' + cardExp, '%d%m/%y').date(), billaddress))

                # Create OrderedItems Entity
                for row in results:
                    query = "INSERT INTO OrderedItems(OrderID, ItemID, Quantity) values(%s, %s, %s)"
                    cursor.execute(query, (orderid, row[1], row[2]))
                    query = "UPDATE Item SET Quantity = Quantity - %s WHERE ItemID = %s"
                    cursor.execute(query, (row[2], row[1]))

                # Delete orders from shopping cart
                query = "DELETE FROM ShoppingCart WHERE CustomerID = %s"
                cursor.execute(query, loggedinid)

                client.commit()
                ordersuccessful = True
                lastorderid = orderid
            except Exception:
                print("Could not complete order action")
                client.rollback()
            finally:
                client.close()
        else:
            itemid = request.form['itemid']
            client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
            try:
                # For things on the right side of the checkout page
                cursor = client.cursor()
                if 'add' in request.form:
                    query = "UPDATE ShoppingCart SET Quantity = Quantity + 1 WHERE CustomerID = %s AND ItemID = %s"
                    cursor.execute(query, (loggedinid, itemid))

                    # Check if user cannot add any more quantity of item
                    query = "SELECT Quantity FROM ShoppingCart WHERE CustomerID = %s AND ItemID = %s"
                    cursor.execute(query, (loggedinid, itemid))
                    currentamount = cursor.fetchall()
                    query = "SELECT Quantity FROM Item WHERE ItemID = %s"
                    cursor.execute(query, itemid)
                    itemamount = cursor.fetchall()
                    if currentamount == itemamount:
                        addbtn = False
                elif 'remove' in request.form:
                    query = "UPDATE ShoppingCart SET Quantity = Quantity - 1 WHERE CustomerID = %s AND ItemID = %s"
                    cursor.execute(query, (loggedinid, itemid))

                    # Delete from shopping cart if quantity = 0
                    query = "DELETE FROM ShoppingCart WHERE CustomerID = %s AND Quantity = 0"
                    cursor.execute(query, loggedinid)

                query = "SELECT I.ItemType, S.Quantity, I.ItemDesc, I.Price, S.ItemID " \
                        "FROM Item I, ShoppingCart S WHERE S.CustomerID = %s AND I.ItemID = S.ItemID"
                cursor.execute(query, loggedinid)
                items = cursor.fetchall()

                hasmembership = 'Y'
                query = "SELECT HasMembership FROM Customer WHERE CustomerID = %s AND HasMembership = %s"
                cursor.execute(query, (loggedinid, hasmembership))
                currentcust = cursor.fetchall()

                # Get discounts and no shipping fee if member
                total = 0
                quantity = 0
                discount = 0
                shipment = 5
                ismember = False
                for row in currentcust:
                    ismember = True

                if ismember:
                    valid = 'Y'
                    query = "SELECT DiscountPercent FROM Discount WHERE Valid = %s"
                    cursor.execute(query, valid)
                    discountvalues = cursor.fetchall()
                    for row in discountvalues:
                        discount += row[0]
                    shipment = 0

                # Get sum of prices
                for row in items:
                    total += row[1] * row[3]
                    quantity += row[1]

                total -= (total * discount)
                total += shipment
                client.commit()
            except Exception:
                print("Could not complete item action")
                client.rollback()
            finally:
                client.close()

    total = round(total, 2)
    discount *= 100
    discount = round(discount, 2)
    if total <= 0:
        total = 0
    if ordersuccessful:
        return redirect('/thankyou.html')
    return render_template('checkout.html', loggedin=loggedinname, items=items, quantity=quantity, total=total,
                           discount=discount, shipment=shipment, addbtn=addbtn, title='Shopping Cart',
                           styles='checkout.css', bodyclass='bg-light')


@app.route("/shop.html", methods=['GET', 'POST'])
def shop():
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT ItemType, Price, ItemDesc, ItemID, Quantity, Seller FROM Item"
        cursor.execute(query)
        if 'category' in request.args:
            query = "SELECT ItemType, Price, ItemDesc, ItemID, Quantity, Seller FROM Item WHERE Category = %s"
            cursor.execute(query, request.args['category'])
        result = cursor.fetchall()

        query = "SELECT Category FROM Item GROUP BY Category"
        cursor.execute(query)
        category = cursor.fetchall()
    except Exception:
        print("Can not retrieve specified Item Entity")
    finally:
        client.close()

    return render_template('shop.html', loggedin=loggedinname, title='Shop', category=category, data=result, styles='',
                           bodyclass='bg-light')


@app.route("/item.html", methods=['GET', 'POST'])
def item():
    if request.method == 'POST':
        itemid = request.form['item']
        if 'cart' in request.form:
            insertShoppingCart(loggedinid, itemid, 1)
        elif 'wishlist' in request.form:
            insertWishList(loggedinid, itemid)
            
    if 'type' and 'price' and 'desc' and 'id' in request.args:
        return render_template('item.html', type=request.args['type'], price=request.args['price'],
                               desc=request.args['desc'], id=request.args['id'], loggedin=loggedinname,
                               employee=None, title=request.args['type'], styles='', bodyclass='bg-light')
    else:
        return render_template('item.html', loggedin=loggedinname, title='[Item Name]', styles='', bodyclass='bg-light')


@app.route("/profile.html")
def profile():
    result = ['NO USER']
    if loggedinid != None:
        result = [loggedinname]
    else:
        return redirect('/')
    return render_template('profile.html', name=result, loggedin=loggedinname, title='Profile', styles='',
                           bodyclass='bg-light')


@app.route("/history.html")
def history():
    result = None
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT O.OrderDate, O.Completed, I.ItemID, I.ItemType, I.Price " \
                "FROM Orders O, OrderedItems S, Item I " \
                "WHERE O.CustomerID = %s AND O.OrderNum = S.OrderID AND S.ItemID = I.ItemID"
        cursor.execute(query, loggedinid)
        result = cursor.fetchall()
    except Exception:
        print("Can not retrieve specified information")
    finally:
        client.close()
    return render_template('history.html', values=result, loggedin=loggedinname, title='Order History', styles='returns.css',
                           bodyclass='bg-light')


@app.route("/wishlist.html", methods=['GET', 'POST'])
def wishlist():
    global loggedinid
    if request.method == 'POST':
        itemid = request.form['item']
        if 'cart' in request.form:
            insertShoppingCart(loggedinid, itemid, 1)
        elif 'remove' in request.form:
            client = pymysql.connect("localhost", "public", "password123", "eCommerce01")

            try:
                cursor = client.cursor()
                query = "DELETE FROM WishList WHERE CustomerID = %s AND ItemID = %s"
                cursor.execute(query, (loggedinid, itemid))
                client.commit()
            except Exception:
                print("Can not retrieve specified information")
            finally:
                client.close()
    result = None
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT I.ItemID, I.ItemType, I.Price " \
                "FROM Wishlist W,  Item I " \
                "WHERE W.CustomerID = %s AND W.ItemID = I.ItemID"
        cursor.execute(query, loggedinid)
        result = cursor.fetchall()
    except Exception:
        print("Can not retrieve specified information")
    finally:
        client.close()
    return render_template('wishlist.html', values= result, loggedin=loggedinname, title='Wish List', styles='returns.css',
                           bodyclass='bg-light')


@app.route("/premium.html")
def premium():
    return render_template('premium.html', loggedin=loggedinname, title='Premium', styles='wishlist.css', bodyclass='bg-light')


@app.route("/address.html")
def address():
    return render_template('address.html', loggedin=loggedinname, title='Address', styles='wishlist.css', bodyclass='bg-light')


@app.route("/payment.html")
def payment():
    return render_template('payment.html', loggedin=loggedinname, title='Payment', styles='wishlist.css', bodyclass='bg-light')


@app.route("/settings.html")
def settings():
    return render_template('settings.html', loggedin=loggedinname, title='Settings', styles='settings.css', bodyclass='bg-light')


@app.route("/returns.html")
def returns():
    return render_template('returns.html', loggedin=loggedinname, title='Returns', styles='returns.css', bodyclass='bg-light')


@app.route("/thankyou.html")
def thankyou():
    results = None
    if lastorderid == None:
        return redirect('/')
    else:
        client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
        try:
            cursor = client.cursor()
            query = "SELECT O.ItemID, O.Quantity, I.Price, I.ItemType, I.ItemDesc " \
                "FROM OrderedItems O, Item I WHERE O.OrderID = %s AND O.ItemID = I.ItemID"
            cursor.execute(query, lastorderid)
            results = cursor.fetchall()
        except Exception:
            print("Could not retrieve specified OrderedItems Entity")
        finally:
            client.close()
    return render_template('thankyou.html', loggedin=loggedinname, results=results, orderid=lastorderid, title='Thank You',
                           styles='thankyou.css', bodyclass='bg-light')

@app.route("/pendingorder.html")
def pendingorder():
    return render_template('pendingorder.html', loggedin=loggedinname, title='Pending Orders', styles='returns.css', bodyclass='bg-light')


'''
BELOW ARE ALL THE METHODS FOR GETTING AND SETTING DATA FROM THE DATABASE
'''


def insertPerson(idvar, email, name, birthdate, phone, address, datejoined, isemployee):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Person(ID, Email, Named, DateOfBirth, Phone, Address, DateJoined, IsEmployee)\
            values(%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (idvar, email, name, birthdate, phone, address, datejoined, isemployee))
        client.commit()
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
def insertCustomer(idvar, userpass, hasmembership):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Customer(CustomerID, Userpass, HasMembership) values(%s, %s, %s)"
        cursor.execute(query, (idvar, userpass, hasmembership))
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
        query = "SELECT CustomerID, Userpass, HasMembership FROM Customer WHERE CustomerID = %s"
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
        query = "SELECT CustomerID, Userpass, HasMembership FROM Customer"
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
def insertItem(itemid, quantity, price, itemtype, seller, itemdesc, category):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Item(ItemID, Quantity, Price, ItemType, Seller, ItemDesc, Category) \
            values(%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (itemid, quantity, price, itemtype, seller, itemdesc, category))
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
        query = "SELECT ItemID, Quantity, Price, ItemType, Seller, ItemDesc, Category FROM Item WHERE ItemID = %s"
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
        query = "SELECT ItemID, Quantity, Price, ItemType, Seller, ItemDesc, Category FROM Item"
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
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT CustomerID, ItemID, Quantity FROM ShoppingCart WHERE CustomerID = %s AND ItemID = %s"
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
        query = "SELECT CustomerID, ItemID, Quantity FROM ShoppingCart"
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
        query = "INSERT INTO WishList(CustomerID, ItemID) values(%s, %s)"
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
def insertDiscount(discountid, discountpercent, valid):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Discount(DiscountID, DiscountPercent, Valid) values(%s, %s, %s)"
        cursor.execute(query, (discountid, discountpercent, valid))
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
        query = "SELECT DiscountID, DiscountPercent, Valid FROM Discount WHERE DiscountID = %s"
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
        query = "SELECT DiscountID, DiscountPercent, Valid FROM Discount"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve Discount Table data")
    finally:
        client.close()


# Orders Table
def insertOrders(orderid, customerid, orderdate, completed, discountid, ordername, orderemail):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Orders(OrderNum, CustomerID, OrderDate, Completed, DiscountID, OrderName, OrderEmail) \
                values(%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (orderid, customerid, orderdate, completed, discountid, ordername, orderemail))
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
        query = "SELECT OrderNum, CustomerID, OrderDate, Completed, DiscountID, OrderName, OrderEmail FROM Orders \
                WHERE OrderNum = %s"
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
        query = "SELECT OrderNum, CustomerID, OrderDate, Completed, DiscountID, OrderName, OrderEmail FROM Orders"
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
def insertPayment(orderid, cardname, cardnum, cardcomp, cardexp, billing):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Payment(OrderID, CardName, CardNum, CardComp, CardExp, Billing) \
                values(%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (orderid, cardname, cardnum, cardcomp, cardexp, billing))
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
        query = "SELECT OrderID, CardName, CardNum, CardComp, CardExp, Billing FROM Payment \
                WHERE OrderID = %s"
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
        query = "SELECT OrderID, CardName, CardNum, CardComp, CardExp, Billing FROM Payment"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve Payment Table data")
    finally:
        client.close()


# Shipment Table
def insertShipment(orderid, address, fee, company, shipname):
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "INSERT INTO Shipment(OrderID, Address, Fee, Company, ShipName) values(%s, %s, %s, %s, %s)"
        cursor.execute(query, (orderid, address, fee, company, shipname))
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
        query = "SELECT OrderID, Address, Fee, Company, ShipName FROM Shipment WHERE OrderID = %s"
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
        query = "SELECT OrderID, Address, Fee, Company, ShipName FROM SHIPMENT"
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


# to run in python
if __name__ == '__main__':
    app.run(debug=True)
