from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mysecretkey'

cnn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "30696222",
    database = "DB_Inventory"
)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/table_edit/<string:id>")
def edit(id):
    cur = cnn.cursor()
    cur.execute(f'SELECT * FROM inventorytable2 WHERE id = {id}')
    data = cur.fetchall()
    print(data[0])
    print(type(data))
    return render_template("table_edit.html", item_information = data[0])

@app.route("/table_update/<string:id>", methods = ['POST'])
def table_update(id):
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        cur = cnn.cursor()
        cur.execute(f'UPDATE inventorytable2 SET name = %s, price = %s WHERE id = {id}', (name, price))
        cnn.commit()
        flash('Contact Upadated susscefullly')
    return redirect(url_for("table_view"))

@app.route("/table_view")
def table_view():
    cur = cnn.cursor()
    cur.execute('SELECT * FROM inventorytable2')
    data = cur.fetchall()
    print(data)
    return render_template("table_view.html", itemInformation = data)


@app.route("/addItem", methods=['POST', 'GET'])
def addItem():
    if request.method == "POST":
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        cur = cnn.cursor()
        cur.execute('INSERT INTO usersTable (name, lastname, email, password) VALUES(%s, %s, %s, %s)',(name, lastname, email, password))
        cnn.commit()
    return redirect(url_for("table_view"))
    


if __name__ == "__main__":
    app.run(port=3000, debug=True)
