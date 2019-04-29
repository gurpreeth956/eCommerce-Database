from flask import Flask, render_template

# do hard refresh on web page if something not loading
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html', styles = 'album.css', bodyclass = 'bg-light')

@app.route("/signup.html")
def signup():
    return render_template('signup.html', styles= 'signin.css', bodyclass= 'text-center')

@app.route("/signin.html")
def login():
    return render_template('signin.html', styles= 'signin.css', bodyclass= 'text-center')

@app.route("/checkout.html")
def checkout():
    return render_template('checkout.html', styles= 'form-validation.css', bodyclass= 'bg-light')

@app.route("/shop.html")
def shop():
    return render_template('shop.html', styles= '', bodyclass= 'bg-light')

@app.route("/item.html")
def item():
    return render_template('item.html', styles= '', bodyclass= 'bg-light')

# to run in python
if __name__ == '__main__':
    app.run(debug = True)