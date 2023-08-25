import sqlite3

class DBAccess:
    def __init__(self, ruta="glosario.db"):
        self.con = sqlite3.connect(ruta)
        self.cursor = self.con.cursor()


    def view_word(self, id):
        sql= f"SELECT * FROM palabra where id={id};"
        self.cursor.execute(sql)
        self.con.commit()
        return self.cursor.fetchone()

    def agregar_palabra(self, esp, eng, us):
        sql = f'INSERT INTO palabra(english,spanish,id_usuario) VALUES ("{eng}","{esp}",{us})'
        self.cursor.execute(sql)
        self.con.commit()
        return self.cursor.lastrowid

    def agregar_usuario(self, last_name, email, cell_phone, teacher_or_student):
        sql = f'INSERT INTO usuario(last_name ,email, cell_phone, teacher_or_student) VALUES ("{last_name}","{email}","{cell_phone}","{teacher_or_student}")'
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

    def load_all_palabra(self):
        self.cursor.execute("SELECT * FROM palabra")
        self.con.commit()
        return self.cursor.fetchall()

    def load_all_meaning(self):
        self.cursor.execute("SELECT * FROM significado")
        self.con.commit()
        return self.cursor.fetchall()
