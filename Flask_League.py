from flask import Flask,g, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = 'FLask_League.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/champions")
def champions():
    cursor = get_db().cursor()
    sql = "SELECT * from champions"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("champions.html", results=results)

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        cursor = get_db().cursor()
        sql = "INSERT INTO champions(Name,Class,MainRole,Description,image_filename) VALUES (?,?,?,?,?)"
        new_name = request.form["Name"]
        new_class = request.form["Class"]
        new_mainrole = request.form["Mainrole"]
        new_description = request.form["Description"]
        new_image = request.form["image_filename"]
        cursor.execute(sql,(new_name,new_class,new_mainrole,new_description,new_image))
        get_db().commit
    return redirect("/champions")
        
    


if __name__ == "__main__":
    app.run(debug=True)
