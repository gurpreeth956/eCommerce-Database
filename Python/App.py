from flask import Flask, render_template, request, redirect
import pymysql.cursors


# do hard refresh on web page if something not loading
app = Flask(__name__)

loggedin = None

@app.route("/")
def home():
    global loggedin
    return render_template('index.html', loggedin= loggedin, title= 'Home', styles = 'album.css', bodyclass = 'bg-light')


@app.route("/signup.html", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        #NEED A UNIQUE GLOBAL NUM
        idn = 0
        # Connect to the database
        client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
        name = request.form['firstName']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        try:
            idn += 1
            cursor = client.cursor()
            query = "INSERT INTO Person(ID, Email, Named, DateOfBirth, Phone, Address, DateJoined, IsEmployee)\
                values(%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (idn, email, name, '1998-11-25', phone, 'Ithaca', '1998-11-25', 'N'))
            client.commit()
        except Exception:
            print(Exception)
            client.rollback()
        finally:
            client.close()
    else:
        print("error")
    return render_template('signup.html', title='Sign Up',  styles='signin.css', bodyclass='text-center')


@app.route("/signin.html", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
        try:
            cursor = client.cursor()
            query = "SELECT P.Email, C.Userpass, C.Username, C.CustomerID, P.ID FROM Customer C, Person P WHERE \
                C.CustomerID = P.ID"
            cursor.execute(query)
            result = cursor.fetchall()
            for customer in result:
                if customer[0] == email and customer[1] == password:
                    global loggedin
                    loggedin = customer[2]
                    print('Logged In')
                    break
            if loggedin != None:
                return redirect('/')
        except Exception:
            print("Can not retrieve specified Customer Entity")
        finally:
            client.close()
    return render_template('signin.html', title='Log In', styles='signin.css', bodyclass='text-center')


@app.route("/checkout.html")
def checkout():
    global loggedin
    return render_template('checkout.html', loggedin= loggedin, title= 'Shopping Cart', styles= 'checkout.css', bodyclass= 'bg-light')


@app.route("/shop.html", methods=['GET', 'POST'])
def shop():
    global loggedin
    # Example of how to get data from database to html file
    client = pymysql.connect("localhost", "public", "password123", "eCommerce01")
    try:
        cursor = client.cursor()
        query = "SELECT ItemType, Price, ItemDesc, ItemID, Quantity, Seller FROM Item"
        cursor.execute(query)
        result = cursor.fetchall()

    except Exception:
        print("Can not retrieve specified Item Entity")
    finally:
        client.close()
    return render_template('shop.html', loggedin= loggedin, title='Shop', data=result, styles='', bodyclass='bg-light')


@app.route("/item.html", methods=['GET', 'POST'])
def item():
    if 'type' and 'price' and 'desc' in request.args:
        return render_template('item.html', type= request.args['type'], price= request.args['price'],
                               desc= request.args['desc'], loggedin= loggedin, title='[Item Name]', styles= '', bodyclass= 'bg-light')
    else:
        return render_template('item.html', loggedin= loggedin, title='[Item Name]', styles= '', bodyclass= 'bg-light')

@app.route("/profile.html")
def profile():
    return render_template('profile.html', loggedin= loggedin, title='Profile', styles='', bodyclass='bg-light')


@app.route("/history.html")
def history():
    return render_template('history.html', loggedin= loggedin, title='Order History', styles='history.css', bodyclass='bg-light')


@app.route("/wishlist.html")
def wishlist():
    return render_template('wishlist.html', loggedin= loggedin, title='Wish List', styles='wishlist.css', bodyclass='bg-light')


# to run in python
if __name__ == '__main__':
    app.run(debug=True)
