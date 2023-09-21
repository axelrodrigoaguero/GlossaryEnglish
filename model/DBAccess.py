import psycopg2


class DBAccess:
    def __init__(self):
        self.con = psycopg2.connect(host="ep-lingering-feather-96861659.us-east-2.aws.neon.tech", database="glosario", user="axelrodrigoaguero", password="DeC9xRSAOjy0")
        self.cursor = self.con.cursor()

    def view_word(self, id):
        self.cursor.execute(f"SELECT * FROM palabra WHERE id= '{id}';")
        self.con.commit()
        return self.cursor.fetchone()

    def view_meaning(self, id_palabra):
        self.cursor.execute(f"SELECT * FROM significado WHERE id_palabra= '{id_palabra}';")
        self.con.commit()
        return self.cursor.fetchall()

    def agregar_palabra(self, eng, esp, us, sta) :
        sql = "INSERT INTO palabra(english, spanish, id_usuario, state) VALUES (%s, %s, %s, %s) RETURNING id;"
        values = (eng, esp, us, sta)
        self.cursor.execute(sql, values)
        self.con.commit()
        id_palabra = self.cursor.fetchone()[0]
        return id_palabra

    def agregar_usuario(self, last_name, email, password, teacherstudent):
        self.cursor.execute(f"INSERT INTO usuario(last_name ,email, password, id_rol) VALUES ('{last_name}','{email}','{password}','{teacherstudent}');")
        self.con.commit()

    def agregar_significado(self, sp, en, id_palabra):
        self.cursor.execute(f"insert into significado(english,spanish,id_palabra) VALUES ('{sp}','{en}',{id_palabra});")
        self.con.commit()


    def delete_palabra(self, id):
        self.cursor.execute( f"DELETE FROM palabra WHERE id=('{id}');")
        self.con.commit()

    def delete_significado(self, id):
        self.cursor.execute(f"DELETE FROM significado WHERE id_palabra=('{id}');")
        self.con.commit()

    def update_word(self, en, es, id):
        self.cursor.execute(f"UPDATE palabra  SET english = '{en}' , spanish = '{es}' WHERE id={id};")
        self.con.commit()

    def update_meaning(self, en, es, id):
        self.cursor.execute(f"UPDATE significado  SET english = '{en}' , spanish = '{es}' WHERE id={id};")
        self.con.commit()

    def get_email_password(self, correo, contrasena):
        self.cursor.execute(f"SELECT * FROM usuario WHERE email ='{correo}' AND password ='{contrasena}';")
        self.con.commit()
        return self.cursor.fetchone()

    def load_all_palabra(self):
        self.cursor.execute(f"SELECT * FROM palabra;")
        self.con.commit()
        return self.cursor.fetchall()

    def load_all_meaning(self):
        self.cursor.execute(f"SELECT * FROM significado;")
        self.con.commit()
        return self.cursor.fetchall()

    def load_words_by_state(self, state):
        self.cursor.execute(f"SELECT * FROM palabra WHERE state = '{state}';")
        return self.cursor.fetchall()

    def load_words_by_user(self, user_id):
        self.cursor.execute(f"SELECT * FROM palabra WHERE id_usuario = '{user_id}';")
        return self.cursor.fetchall()

    def confirmed_word(self, id, estado):
        self.cursor.execute(f"UPDATE palabra  SET state = '{estado}' WHERE id={id};")
        self.con.commit()


