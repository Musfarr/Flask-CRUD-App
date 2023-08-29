from flask import Flask, render_template, app ,request , url_for , redirect
from flask_mysqldb import MySQL


app = Flask(__name__)


## database connection to flask
mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'test'





@app.route('/')
def home():
    return render_template("index.html")




@app.route('/firstroute')
def firstRoute():
    # {'name': 'abc', 'age': 90, 'country': 'Paksitan'}

#data coming from datatbase inform of tuples

    name = []
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM emp")
    data = cur.fetchall()
    cur.close()

#converting tuples into list of dictionaries
    for i in data:
        name.append({"name": i[0] , "age" : i[1] , "num":i[2] })
    print(name)
    return render_template("main.html",name=name)




@app.route('/secondroute')
def secondroute():
    return render_template("form.html")




@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        id = request.form['id']
        username = request.form['fname']
        num = request.form['lname']

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO emp (id, name , number) VALUES (%s, %s , %s)", (id, username , num))

        mysql.connection.commit()
        cur.close()
        return render_template("index.html")



@app.route("/delform")
def delform():
    return render_template("delform.html")



@app.route('/delete', methods=['get'])
def delete():
    if request.method == 'GET':
        # Access the "eid" parameter from the query string
        id = request.args.get('eid')

        cur = mysql.connection.cursor()

        # Execute the DELETE query
        delete_query = "DELETE FROM emp WHERE id = %s"
        cur.execute(delete_query, (id,))

        # Commit the transaction
        mysql.connection.commit()
        cur.close()

        return render_template('main.html')

    return "Invalid request"





@app.route("/formupdate")
def formupdate():
    return render_template("update.html")





@app.route("/update", methods=['POST'])
def update():
    if request.method == 'POST':
        id = request.form['eid']
        name = request.form['name']
        num = request.form['num']

        cur = mysql.connection.cursor()
        update_query = "UPDATE emp SET name = %s, number = %s WHERE id = %s"
        cur.execute(update_query, (name, num, id))
        mysql.connection.commit()
        cur.close()

        return 'Success'  # Return a success message

    return "Invalid request"




if __name__ == '__main__':
    app.run(debug=True)


