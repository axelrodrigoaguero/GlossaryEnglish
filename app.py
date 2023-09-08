from flask import Flask, render_template, request, url_for, flash, session, redirect
import sqlite3

from model.DBAccess import DBAccess



connection =sqlite3.connect("DBAccess.py")
app = Flask(__name__)

app.secret_key= 'mysecertkey'

#Pagina Principal
@app.route("/")
def inicio():

    return render_template("home.html")

#Pagina Formulario Nuevo Usuario
@app.route("/new_user")
def new_user():

   return render_template("new_user.html")

#Funcion de Guardar Nuevo Usuario

@app.route("/check_in", methods = ['POST'])
def new_user_create():
    if request.method == "POST":
        db = DBAccess("database/glosario.db")
        name = request.values.get("firstname")
        email = request.values.get("email")
        password = request.values.get("password")
        teacher_or_student = request.values.get("teacher_or_student")

        if not name or not email or not password or not teacher_or_student :
            flash("All fields are required. Please fill them all out.")
            return redirect(url_for("new_user"))

        nuevo_id = db.agregar_usuario(name, email, password,teacher_or_student)
        flash("User Saved")
        return app.redirect(url_for("new_user"))

    return app.redirect(url_for("new_user"))

#Pagina de Inicio de Session

@app.route("/login")
def login():
    return render_template("login.html")

#Funcion Iniciar Session

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


            return render_template("home.html")

        else:
            flash("Email of Password Invalid")
            return render_template("login.html")

    return render_template("login.html")

#Funcion Cerrar Session

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

#Pagina Listado de Palabras

@app.route("/my_words")
def my_words():
    id_rol = session.get('id_rol')

    db = DBAccess("database/glosario.db")


    if id_rol == 1 :
        words= db.load_words_by_state("pendiente")
        return render_template("my_words.html", words=words)
    elif id_rol == 2 :
        user_id = session.get('id')
        words = db.load_words_by_user(int(user_id))
        return render_template("my_words.html", words=words)
    else :
        words= db.load_words_by_state("confirmada")
        return render_template("my_words.html", words=words)

#Pagina Ver una palabra

@app.route("/show_word/<id>")
def show_word(id):
    db = DBAccess("database/glosario.db")
    word= db.view_word(int(id))
    meanings= db.view_meaning(int(id))
    return render_template("show_word.html", word= word, meanings= meanings)

#Pagina de Formulario Nueva Palabra

@app.route("/new_word")
def new_word():
    return render_template("new_word.html")

#Funcion de Guardar Nueva Palabra

@app.route("/save_word", methods = ['POST'])
def save_word():
    if request.method == "POST":
        db = DBAccess("database/glosario.db")
        word = request.values.get("word")
        spanish = request.values.get("spanish")
        if not word or not spanish:
            flash("All fields are required. Please fill them all out.")
            return redirect(url_for("new_word"))
        nuevo_id = db.agregar_palabra(word, spanish,1,"pendiente")
        meaning= request.values.get("meaning")
        spanish_meaning = request.values.get("spanish_meaning")
        db.agregar_significado(meaning, spanish_meaning,  nuevo_id)
        flash("Word Saved")
        return app.redirect(url_for("new_word"))
    return render_template("new_word.html")

#Funcion Eliminar Palabra

@app.route('/delete_word/<string:id>')
def delete_word(id):
    db = DBAccess("database/glosario.db")
    db.delete_palabra(id)
    db.delete_significado(id)
    flash("Delete Word")
    words = db.load_all_palabra()
    return render_template("my_words.html",words=words)

#Pagina de Formulario Nuevo Significado
@app.route('/add_meaning/<string:id>')
def add_meaning(id):
    id= int(id)
    return render_template("add_new_meaning.html",id= id)

@app.route('/new_meaning/<string:id>', methods = ['POST'])
def new_meaning(id):
    if request.method == "POST" :
        print(id)
        db = DBAccess("database/glosario.db")
        meaning = request.values.get("meaning")
        spanish_meaning = request.values.get("spanish_meaning")

        if not meaning or not spanish_meaning:
            flash("All fields are required. Please fill them all out.")
            return redirect(url_for("new_word"))
        db.agregar_significado(meaning, spanish_meaning, id)
        return app.redirect(url_for("my_words"))


app.run(debug=True)
