from flask import Flask, render_template, request, url_for, flash, Response, session
import sqlite3

from model.DBAccess import DBAccess



connection =sqlite3.connect("DBAccess.py")
app = Flask(__name__)

app.secret_key= 'mysecertkey'

@app.route("/")
def inicio():
    return render_template("home.html")


@app.route("/new_word")
def new_word():
    return render_template("new_word.html")


@app.route("/my_words")
def my_words():
    db = DBAccess("database/glosario.db")
    words = db.load_all_palabra()
    return render_template("my_words.html",words=words)


@app.route("/save_word", methods = ['POST'])
def save_word():
    if request.method == "POST":
        db = DBAccess("database/glosario.db")
        word = request.values.get("word")
        spanish = request.values.get("spanish")
        nuevo_id = db.agregar_palabra(spanish,word,1,"pendiente")
        meaning= request.values.get("meaning")
        spanish_meaning = request.values.get("spanish_meaning")
        nuevo_id = db.agregar_significado(meaning, spanish_meaning,  nuevo_id)
        flash("Word Saved")
        return app.redirect(url_for("new_word"))
    return render_template("new_word.html")


@app.route("/new_user")
def new_user():
   return render_template("New_User.html")



@app.route("/new_user/create", methods = ['POST'])
def new_user_create():
    if request.method == "POST":
        db = DBAccess("database/glosario.db")
        name = request.values.get("firstname")
        email = request.values.get("email")
        password = request.values.get("password")
        teacher_or_student = request.values.get("teacher_or_student")
        nuevo_id = db.agregar_usuario(name, email, password,teacher_or_student)
        flash("User Saved")
        return app.redirect(url_for("new_user"))

    return "ok"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logeo", methods = ['GET','POST'])
def logeo():
    if request.method == "POST" and 'email' in request.form and 'password':
        email= request.form['email']
        password = request.form['password']
        db = DBAccess("database/glosario.db")
        account= db.get_email_password(email,password)
        if account:
            session['logueado'] = True
            session['id'] = account[0]
            session['id_rol'] = account[4]

            if session['id_rol'] == 2:
                return render_template("teacher.html")
            elif session['id_rol'] == 1:
                return render_template("student.html")
        else:
            flash("Email of Password Invalid")
            return render_template("login.html")

    return render_template("login.html")



@app.route("/show_word/<id>")
def show_word(id):
    db = DBAccess("database/glosario.db")
    word= db.view_word(int(id))
    return render_template("show_word.html", word= word)


@app.route('/delete_word/<string:id>')
def delete_word(id):
    db = DBAccess("database/glosario.db")
    db.delete_palabra(id)
    flash("Delete Word")
    words = db.load_all_palabra()
    return render_template("my_words.html",words=words)

app.run(debug=True)
