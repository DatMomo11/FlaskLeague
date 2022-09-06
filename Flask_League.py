from flask import Flask,g, render_template, request, redirect, flash,url_for
import sqlite3, os
from werkzeug.utils import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DATABASE = 'Flask_League.db'

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
    sql = "SELECT * from champions join classes on champions.Class = classes.id join roles on champions.Role = roles.id join images on champions.image_filename = images.id" 
    cursor.execute(sql)
    results = cursor.fetchall()
    
    cursor = get_db().cursor()
    sql = "SELECT * from classes" 
    cursor.execute(sql)
    classes = cursor.fetchall()
    
    cursor = get_db().cursor()
    sql = "SELECT * from champions join roles on champions.Role = roles.id;" 
    cursor.execute(sql)
    role_results = cursor.fetchall()
    
    cursor = get_db().cursor()
    sql = "SELECT * from roles" 
    cursor.execute(sql)
    role = cursor.fetchall()
    
    cursor = get_db().cursor()
    sql = "SELECT * from images" 
    cursor.execute(sql)
    images = cursor.fetchall()
    
    
    
     
    return render_template("champions.html", results=results, classes=classes,role_results=role_results,role=role,images=images)


@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        db = get_db()    
        cursor = db.cursor()
        sql = "INSERT INTO champions(Name,Class,Role,Description,image_filename) VALUES (?,?,?,?,?)"
        new_name = request.form["Name"]
        new_class = request.form["Class"]
        new_role = request.form["Role"]
        new_description = request.form["Description"]
        new_image = request.form["image_filename"]
        cursor.execute(sql,(new_name,new_class,new_role,new_description,new_image))
        db.commit()
    return redirect("/champions")

'''@app.route('/delete', methods=["GET","POST"])
def delete():
    if request.method == "POST":
        cursor = get_db().cursor()
        id = int(request.form["item_name"])
        sql = "DELETE FROM champions WHERE id=?"
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect("/champions")'''



@app.route('/guides')
def guides():
    return render_template("guides.html")

@app.route('/FAQ')
def FAQ():
    return render_template("FAQ.html")

@app.route('/Talon')
def Talon():
    return render_template("Talon.html")
        
    
if __name__ == "__main__":
    app.run(debug=True)
    

