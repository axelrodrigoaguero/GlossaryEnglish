import sqlite3

class DBAccess:
    def __init__(self, ruta="glosario.db"):
        self.con = sqlite3.connect(ruta)
        self.cursor = self.con.cursor()


    def view_word(self, id):
        sql= f"SELECT * FROM palabra WHERE id= {id}"
        self.cursor.execute(sql)
        self.con.commit()
        return self.cursor.fetchone()

    def view_meaning(self, id_palabra):
        sql= f"SELECT * FROM significado WHERE id_palabra={id_palabra}"
        self.cursor.execute(sql)
        self.con.commit()
        return self.cursor.fetchall()

    def agregar_palabra(self, eng, esp,  us,sta):
        sql = f'INSERT INTO palabra(english,spanish,id_usuario,state) VALUES ("{eng}","{esp}",{us},"{sta}")'
        self.cursor.execute(sql)
        self.con.commit()
        return self.cursor.lastrowid

    def agregar_usuario(self, last_name, email, password, teacher_or_student):
        sql = f'INSERT INTO usuario(last_name ,email, password, id_rol) VALUES ("{last_name}","{email}","{password}","{teacher_or_student}")'
        self.cursor.execute(sql)
        self.con.commit()

    def agregar_significado(self, sp, en, id_palabra):
        sql = f'INSERT INTO significado(english,spanish,id_palabra) VALUES ("{sp}","{en}",{id_palabra})'
        self.cursor.execute(sql)
        self.con.commit()
        return self.cursor.lastrowid

    def delete_palabra(self,id):
        sql = f'DELETE FROM palabra WHERE id=("{id}")'
        self.cursor.execute(sql)
        self.con.commit()

    def delete_significado(self,id):
        sql = f'DELETE FROM significado WHERE id=("{id}")'
        self.cursor.execute(sql)
        self.con.commit()

    def update_palabra(self,en, es, id):
        sql = f"UPDATE significado  SET english = '{en}' , spanish = '{es}' WHERE id={id};"
        self.cursor.execute(sql)
        self.con.commit()

    def get_email_password(self, correo, contrasena):
        self.cursor.execute(f"SELECT * FROM usuario WHERE email ='{correo}' AND password ='{contrasena}'")
        self.con.commit()
        return self.cursor.fetchone()

    def load_all_palabra(self):
        self.cursor.execute("SELECT * FROM palabra")
        self.con.commit()
        return self.cursor.fetchall()

    def load_all_meaning(self):
        self.cursor.execute("SELECT * FROM significado")
        self.con.commit()
        return self.cursor.fetchall()

    def load_words_by_state(self, state) :
        self.cursor.execute("SELECT * FROM palabra WHERE state = ?", (state,))
        return self.cursor.fetchall()

    def load_words_by_user(self, user_id) :
        self.cursor.execute("SELECT * FROM palabra WHERE id_usuario = ?", (user_id,))
        return self.cursor.fetchall()

