from flask import Flask, render_template,request,flash, session, redirect, url_for
import sqlite3
from formularios import formActualizar, formCrear, formCambiarContrasena
import os
import hashlib
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
import random
import yagmail as yagmail
import string
import secrets
from db import get_db, close_db
from flask_mail import Mail, Message



app = Flask(__name__)
app.secret_key = os.urandom(24)
posta = Mail(app)
@app.route("/")
def primer():
     if "usuario" in session:
        return render_template("index.html")
     else:
        return "Accion no permitida <a href='/login'>Adiós</a>"

@app.route("/login",methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route("/",methods=["POST","GET"])
def loginPrueba():
    nombre = request.form["usuario"]
    clave = request.form["clave"]
    with sqlite3.connect('BaseDeDatos.db') as con:
        cur = con.cursor()
        user = cur.execute(f"SELECT pwd__4_usr, id_4_usr  FROM Tbl4Usrs WHERE nick_name_4_usr = '{nombre}'").fetchone()
        if user != None:
            clave_hash = user[0]
            idUser = user[1]
            if check_password_hash(clave_hash,clave):
                session["usuario"]=nombre
                session["idUsuario"]=idUser
                return render_template('index.html')
        #cur.execute("SELECT * FROM Tbl4Usrs WHERE nick_name_4_usr = ? AND pwd__4_usr = ?",(nombre,clave))
        #if cur.fetchone():
            #session["usuario"]=nombre
            else: 
                return "Usuario o contraseña inválidos."
        else: 
            return "Usuario o contraseña inválidos."
            
    return "Usuario no permitido"
   
@app.route('/registro.html', methods=["GET"])
def crearRegistroMostrar():
   return render_template('registro.html')

@app.route('/recuperarPassword.html', methods=["GET"])
def crearRecuperarPasswordMostrar():
   return render_template('recuperarpassword.html')

@app.route("/activate", methods=['GET'])
def activate():
    return "activar"


@app.route('/registro.html', methods=["POST"])
def crearRegistroRegistrar():

    nombre = escape(request.form["nombre"])
    email= request.form["email"]
    clave1 = escape(request.form["clave1"])
    clave2 = escape(request.form["clave2"])
    if  clave1 == clave2:
        hashclave = generate_password_hash(clave1)
        try:
            with sqlite3.connect('BaseDeDatos.db') as con: 
                cur = con.cursor()
                number = hex(random.getrandbits(512))[2:]
                cur.execute("INSERT INTO Tbl4Usrs(nick_name_4_usr,email_4_usr,pwd__4_usr,kinda_usr,now_usr_is)VALUES(?,?,?,?,?)",(nombre,email,hashclave,number,"activo"))
                con.commit()

                yag = yagmail.SMTP("pruebatk.8912@gmail.com","prueba123")
                yag.send(to=email,subject="Activa tu cuenta",contents='Bienvenido al link para activar tu cuenta'+url_for('activate',_external=True)+'?auth='+number)
                flash("Revisa tu correo para activar tu cuenta")
                return "Guardado satisfactoriamente"
            #return render_template("login.html")
            print("Llegó al final")  
            return render_template("registro.html")
        except: 
            con.rollback()
    else:
        return "las claves no coinciden"

@app.route("/recuperate", methods=['GET'])
def recuperate():
    return render_template('recuperar.html')

@app.route("/recuperate", methods=['POST'])
def newPassword():
    clave1 = escape(request.form["clave1"])
    clave2 = escape(request.form["clave2"])
    idU = session.get("idUser")

    if  clave1 == clave2:
        hashclave = generate_password_hash(clave1)
        try:
            with sqlite3.connect('BaseDeDatos.db') as con: 
                cur = con.cursor()
                cur.execute(f"UPDATE Tbl4Usrs SET pwd__4_usr = '{hashclave}' WHERE id_4_usr = '{idU}'")
                con.commit()
                flash("Se ha actualizado correctamente")
            return redirect("login")
                    
                    #hashPassword = generate_password_hash(password)
                    #db.execute('UPDATE Tbl4Usrs SET pwd__4_usr = ? WHERE email_4_usr = ?' ,(hashPassword, email))
                    #db.commit()
                
                
                    #cur.execute(f"UPDATE Tbl4Usrs SET pwd__4_usr = '{hashPassword}' WHERE email_4_usr = '{email}'")
                    #cur.commit()
                    
                #return "Guardado satisfactoriamente"
        except:
            return render_template("recuperar.html")


@app.route('/recuperarPassword.html', methods=['POST'])
def recuperarPasswordS():
        try:
            if request.method == 'POST':
                email1 = request.form['email']
                
                with sqlite3.connect('BaseDeDatos.db') as con: 
                    cur = con.cursor()
                    number = hex(random.getrandbits(512))[2:]
                    res = cur.execute(f"SELECT id_4_usr FROM Tbl4Usrs WHERE email_4_usr = '{email1}'").fetchone()
                    cur.execute("INSERT INTO recuperacion(id_usuario,recu)VALUES(?,?)",(res[0],number))
                    con.commit()
                    session["idUser"]=res[0]
                    yag = yagmail.SMTP('pruebatk.8912@gmail.com', 'prueba123') #modificar con tu informacion personal
                    yag.send(to=email1,subject="recupere contraseña",contents='Bienvenido al link para activar tu cuenta'+url_for('recuperate',_external=True)+'?auth='+number)
                    flash("Revisa tu correo para recuperar contraseña")
                    return "Se envio correctamente"
                    
                    #hashPassword = generate_password_hash(password)
                    #db.execute('UPDATE Tbl4Usrs SET pwd__4_usr = ? WHERE email_4_usr = ?' ,(hashPassword, email))
                    #db.commit()
                
                return render_template('recuperarpassword.html')
                    #cur.execute(f"UPDATE Tbl4Usrs SET pwd__4_usr = '{hashPassword}' WHERE email_4_usr = '{email}'")
                    #cur.commit()
                    
                #return "Guardado satisfactoriamente"
        except:
            flash( 'Se ha producido un error, intente de nuevo en unos minutos' )
            return render_template( 'recuperarpassword.html' )

@app.route('/mostrar')
def mostrar():
    return render_template('mostrar.html')

# Rutas de vistas de Raul
@app.route('/index.html')
def inicialIndex():
    return render_template('index.html')

@app.route('/crearBlog', methods=["GET"])
def crearBlogMostrar():
   idUser = session.get("idUsuario")

   if str(idUser) != "None":
    form = formCrear()
    return render_template('crearBlog.html', form=form)
   
   return redirect("login", code=302)

@app.route('/crearBlog', methods=["POST"])
def crearBlogRegistrar():
    idUser = session.get("idUsuario")
    titulo = escape(request.form["titulo"])
    contenido = escape(request.form["contenido"])
    strVisibilidad = escape(request.form["publico"])

    if str(idUser) != "None":
        if len(titulo) != 0 and len(contenido) != 0:

            with sqlite3.connect('BaseDeDatos.db') as con: 
                cur = con.cursor()
                cur.execute("INSERT INTO Tbl4Bgs(id_4_usr_in_bg,head_4_bg,info_4_bg,visibility_4_bg,now_bg_is)VALUES(?,?,?,?,?)",(idUser,titulo,contenido,strVisibilidad,"activo"))
                con.commit()
                return redirect("/MisRegistros", code=302) 
        else:
            return "Asegurese de llenar todos los campos"
    
    return redirect("login", code=302)


@app.route('/cambiarContrasena', methods=["GET"])
def cambiarContrasenaMostrar():
    form = formCambiarContrasena()
    return render_template('cambiarContrasena.html', form=form)

@app.route('/cambiarContrasena', methods=["POST"])
def cambiarContrasenaRegistrar():
    form = formCambiarContrasena()
    idUser = session.get("idUsuario")
    claveActual = escape(request.form["claveActual"])
    claveNueva = escape(request.form["claveNueva"])
    claveNuevaConfirmacion = escape(request.form["claveNuevaConfirmacion"])

    if str(idUser) != "None":
        with sqlite3.connect('BaseDeDatos.db') as con:
            cur = con.cursor()
            user = cur.execute(f"SELECT pwd__4_usr  FROM Tbl4Usrs WHERE id_4_usr = '{idUser}'").fetchone()
            if user != None:
                clave_hash = user[0]

                if check_password_hash(clave_hash,claveActual):
                    if  claveNueva == claveNuevaConfirmacion:
                        hashclaveNueva = generate_password_hash(claveNueva)
                        try:
                            with sqlite3.connect('BaseDeDatos.db') as con: 
                                cur = con.cursor()
                                cur.execute("UPDATE Tbl4Usrs SET pwd__4_usr=? WHERE id_4_usr=?",(hashclaveNueva, idUser))
                                con.commit()
        
                                if con.total_changes>0:
                                    return redirect("login", code=302)
                                else:
                                    return "Falla en el cambio actualizando"

                        
                        except: 
                            con.rollback()
                            return "Falla en el cambio"
                    else:
                        return "La nueva clave no coincide"
                else:
                        return "La clave actual no coincide"

    return redirect("login", code=302)

@app.route('/cerrarSesion', methods=["GET"])
def cerrarSession():
    session.clear()
    return redirect("login", code=302)


# Rutas de vistas de Jorge

@app.route('/MisRegistros', methods=["GET", "POST"])
def misRegistros():
    idUsuario = session.get("idUsuario")
    if str(idUsuario) != "None":
        try: 
            with sqlite3.connect('BaseDeDatos.db') as con:
                con.row_factory = sqlite3.Row 
                cur = con.cursor()
                cur.execute("SELECT * from Tbl4Bgs WHERE id_4_usr_in_bg = ?",[idUsuario]) 
                row = cur.fetchall()
                return render_template('MisRegistros.html',row = row)
        except: 
            return "No se pudo listar"
    #return render_template('MisRegistros.html')
    return redirect("login", code=302) 


@app.route('/Actualizar', methods=["GET","POST"])
def actualizarBlog():
    idUsuario = session.get("idUsuario")
    if str(idUsuario) != "None":
        form = formActualizar()
        if request.method == "POST":
            idblog = 1 #Tengo que modificar. 
            titulo = form.titulo.data
            contenido = form.contenido.data
            publico = form.publico.data
            #privado = form.privado.data
            try:
                with sqlite3.connect('BaseDeDatos.db') as con: 
                    cur = con.cursor()
                    cur.execute("UPDATE Tbl4Bgs SET head_4_bg = ?,info_4_bg=?,visibility_4_bg=? WHERE id_4_bg = ?",[titulo,contenido,publico,idblog])
                    con.commit()
                    if con.total_changes>0:
                        mensaje = "El blog fue actualizado con éxito"
                    else:
                        mensaje = "No se pudo actualizar este blog."
            except: 
                con.rollback()
            finally:
                return mensaje
        #return render_template('Actualizar.html')
    return redirect("login",code=302)
    
@app.route('/Actualizar/Actualizado')
def blogActualizado():
    idUsuario = session.get("idUsuario")
    if str(idUsuario) != "None":
        return render_template('PopUpActualizar.html')
    return redirect("login",code=302)

@app.route('/Actualizar/Eliminar', methods = ['GET','POST'])
def blogEliminar():
    idUsuario = session.get("idUsuario")
    if str(idUsuario) != "None":
        form = formActualizar()
        idblog = 1 #Tengo que modificar. 
        try:
            with sqlite3.connect('BaseDeDatos.db') as con:
                con.row_factory = sqlite3.Row 
                cur = con.cursor()
                cur.execute("DELETE from Tbl4Bgs where id_4_bg = ?",[idblog]) 
                if con.total_changes>0: 
                    mensaje = "Blog Eliminado"
                else:
                    mensaje = "Blog no encontrado"
        except:
            mensaje = "Error"
        finally:
            return mensaje
        return "No existe ese blog en el registro" 
        #return render_template('PopUpEliminar.html')
    return redirect("login",code=302)

# @app.route('/Actualizar/Eliminar', methods = ['GET','POST'])
# def blogEliminar():
#     form = formActualizar()
#     if request.method == "POST":
#         idblog = 1 #Tengo que modificar. 
#         try:
#             with sqlite3.connect('BaseDeDatos.db') as con: 
#                 cur = con.cursor()
#                 cur.execute("UPDATE Tbl4Bgs SET now_bg_is = 'False' WHERE id_4_bg = ?",[idblog])
#                 con.commit()
#                 if con.total_changes>0:
#                     mensaje = "El blog fue eliminado"
#                 else:
#                     mensaje = "No se pudo eliminar este blog."
#         except: 
#             con.rollback()
#         finally:
#             return mensaje

@app.route('/Eliminado')
def blogEliminado(): 
    idUsuario = session.get("idUsuario")
    if str(idUsuario) != "None":
        return render_template('PopUpEliminado.html')
    return redirect("login",code=302)


@app.route('/Buscar')
def buscar():
    iduser = 1 #tengo que modificar
    try: 
        with sqlite3.connect('BaseDeDatos.db') as con:
            con.row_factory = sqlite3.Row 
            cur = con.cursor()
            cur.execute("SELECT * from Tbl4Bgs WHERE id_4_usr_in_bg = ?",[iduser]) 
            row = cur.fetchall()
            return render_template('Buscar.html',row = row)
    except: 
        return render_template('Buscar.html')



@app.route('/comentar',methods = ['GET','POST'])
def comentar():
    try: 
        with sqlite3.connect('BaseDeDatos.db') as con:
                con.row_factory = sqlite3.Row 
                cur = con.cursor()
                cur.execute("SELECT * from Tbl4Comts") 
                row = cur.fetchall()
                return render_template('comentar.html',row = row)
    except: 
        return "No se pudo comentar"



if __name__ == "__main__":
    app.run(debug=True)