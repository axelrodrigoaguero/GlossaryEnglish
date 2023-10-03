from flask import Flask, render_template, request, url_for, flash, session, redirect
import hashlib
from model.DBAccess import DBAccess

db= DBAccess()

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

@app.route("/check_in", methods=['POST'])
def new_user_create():
    if request.method == "POST":
        name = request.values.get("firstname")
        email = request.values.get("email")
        password = request.values.get("password")
        teacher_or_student = request.values.get("teacher_or_student")

        if not name or not email or not password or not teacher_or_student:
            flash("All fields are required. Please fill them all out.")
            return redirect(url_for("new_user"))

        hashed_password = hashlib.md5(password.encode()).hexdigest()

        db.agregar_usuario(name, email, hashed_password, teacher_or_student)
        flash("User Saved")
        return redirect(url_for("new_user"))

    return redirect(url_for("new_user"))


#Pagina de Inicio de Session

@app.route("/login")
def login():
    return render_template("login.html")

#Funcion Iniciar Session

@app.route("/logeo", methods=['GET', 'POST'])
def logeo():
    if request.method == "POST" and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        # Hashea la contraseña ingresada con MD5 para compararla con la almacenada
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        account = db.get_email_password(email, hashed_password)  # Compara con la contraseña hasheada
        if account:
            session['logueado'] = True
            session['id'] = account[0]
            session['id_rol'] = account[4]
            return render_template("home.html")

        else:
            flash("Email or Password Invalid")
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
    word= db.view_word(int(id))
    meanings= db.view_meaning(int(id))
    return render_template("show_word.html", word= word, meanings= meanings)

#Pagina Listado de Palabras Confirmadas

@app.route("/my_words_confirm")
def my_words_confirm():
    words = db.load_words_by_state("confirmada")
    return render_template("my_words_confirm.html", words=words)

#Pagina Ver una Palabra Confirmada

@app.route("/show_word_confirm/<id>")
def show_word_confirm(id):
    word= db.view_word(int(id))
    meanings= db.view_meaning(int(id))
    return render_template("show_word_confirm.html", word= word, meanings= meanings)

#Pagina de Formulario Nueva Palabra

@app.route("/new_word")
def new_word():
    return render_template("new_word.html")

#Funcion de Guardar Nueva Palabra

@app.route("/save_word", methods = ['POST'])
def save_word():
    if request.method == "POST":
        id_user= session.get('id')
        word = request.values.get("word")
        spanish = request.values.get("spanish")
        if not word or not spanish:
            flash("All fields are required. Please fill them all out.")
            return render_template("new_word.html")
        id_palabra = db.agregar_palabra(word, spanish,id_user,"pendiente")
        meaning= request.values.get("meaning")
        spanish_meaning = request.values.get("spanish_meaning")
        db.agregar_significado(meaning, spanish_meaning, id_palabra)
        flash("Word Saved")
        return app.redirect(url_for("new_word"))
    return render_template("new_word.html")

#Funcion Eliminar Palabra

@app.route('/delete_word/<string:id>')
def delete_word(id):
    db.delete_palabra(id)
    db.delete_significado(id)
    flash("Delete Word")

    id_rol = session.get('id_rol')

    if id_rol == 1 :
        words = db.load_words_by_state("pendiente")
        return render_template("my_words.html", words=words)
    elif id_rol == 2 :
        user_id = session.get('id')
        words = db.load_words_by_user(int(user_id))
        return render_template("my_words.html", words=words)
    else :
        words = db.load_words_by_state("confirmada")
        return render_template("my_words.html", words=words)

#Funcion Eliminar Significado

@app.route("/delete_meaning/<string:id>/<id_word>")
def delete_meaning(id,id_word):
    db.delete_significado(id)
    flash("Delete Meaning")
    word = db.view_word(int(id_word))
    meanings = db.view_meaning(int(id_word))
    return render_template("show_word.html", word=word, meanings=meanings)


#Pagina de Formulario Nuevo Significado
@app.route('/add_meaning/<string:id>')
def add_meaning(id):
    id= int(id)
    return render_template("add_new_meaning.html",id= id)

#Funcion de Guardar Nuevo Significado

@app.route('/new_meaning/<string:id>', methods = ['POST'])
def new_meaning(id):
    if request.method == "POST" :
        meaning = request.values.get("meaning")
        spanish_meaning = request.values.get("spanish_meaning")

        if not meaning or not spanish_meaning:
            flash("All fields are required. Please fill them all out.")
            return render_template("add_new_meaning.html",id= id)
        db.agregar_significado(meaning, spanish_meaning, id)
        flash("Save Meaning")
        word = db.view_word(int(id))
        meanings = db.view_meaning(int(id))
        return render_template("show_word.html", word=word, meanings=meanings)

#Pagina de Formulario de Actualizar Significado

@app.route('/up_meaning/<string:id>/<id_word>')
def up_meaning(id,id_word):
    id= int(id)
    id_word= id_word

    return render_template("update_meaning.html",id= id,id_word= id_word)

#Funcion de Actualizar Significado

@app.route('/update_meaning/<string:id>/<string:id_word>', methods = ['POST'])
def update_meaning(id ,id_word):
    if request.method == "POST" :
        meaning = request.values.get("meaning")
        spanish_meaning = request.values.get("spanish_meaning")

        word = request.values.get("word")
        spanish = request.values.get("spanish")



        if not meaning or not spanish_meaning:
            flash("All fields are required. Please fill them all out.")
            return render_template("update_meaning.html",id= id,id_word= id_word)

        db.update_meaning(meaning,spanish_meaning,id)
        flash("Update Meaning")
        word = db.view_word(id_word)
        meanings = db.view_meaning(id_word)
        return render_template("show_word.html", word=word, meanings=meanings)

#Pagina de Formulario de Actualizar Palabra

@app.route('/up_word/<string:id>')
def up_word(id):
    id= int(id)
    return render_template("update_word.html",id= id)

#Funcion de Actualizar Palabra

@app.route('/update_word/<string:id>', methods = ['POST'])
def update_word(id):
    if request.method == "POST" :
        word = request.values.get("word")
        spanish = request.values.get("spanish")
        if not word or not spanish:
            flash("All fields are required. Please fill them all out.")
            return render_template("update_word.html",id= id)

        db.update_word(word,spanish,id)
        flash("Update Word")
        word = db.view_word(int(id))
        meanings = db.view_meaning(int(id))
        return render_template("show_word.html", word=word, meanings=meanings)

#Funcion de Confirmar Palabra

@app.route('/confirm_word/<string:id>')
def confirm_word(id):
    estado= "confirmada"
    db.confirmed_word(id, estado)
    id_rol = session.get('id_rol')


    if id_rol == 1 :
        words = db.load_words_by_state("pendiente")
        return render_template("my_words.html", words=words)
    elif id_rol == 2 :
        user_id = session.get('id')
        words = db.load_words_by_user(int(user_id))
        return render_template("my_words.html", words=words)
    else :
        words = db.load_words_by_state("confirmada")
        return render_template("my_words_confirm.html", words=words)

app.run(debug=True)
