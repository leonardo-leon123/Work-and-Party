from flask import Flask, render_template, request, json, redirect, url_for
from flaskext.mysql import MySQL
from json import dumps, loads, JSONEncoder, JSONDecoder
import bcrypt
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['MYSQL_DATABASE_USER'] = 'sepherot_lorena'
app.config['MYSQL_DATABASE_PASSWORD'] = '9LwPFmj9QS'
app.config['MYSQL_DATABASE_DB'] = 'sepherot_lorenaBD'
app.config['MYSQL_DATABASE_HOST'] = 'sepheroth.com'

mysql = MySQL(app)

def InsertUser(_nombre,_apellido,_correo,_contraseña,_user):
    try:
        if _nombre and _apellido and _correo and _contraseña and _user:
            #print("Base de Datos")
            conn=mysql.connect()
            cursor=conn.cursor()
            query="INSERT INTO T_Usuarios (Nombre, Apellido, Correo, Contraseña, Usuario,Onboard) VALUES (%s, %s, %s, %s, %s,'0')"
            cursor.execute(query,(_nombre,_apellido,_correo,_contraseña,_user))
            conn.commit()
            if query:
                return True
            else:
                return False
    except:
        return redirect(url_for("error404"))
    finally:
        conn.close()
        cursor.close()

def Onboarding(_user):
    try:
        if _user:
            conn=mysql.connect()
            cursor=conn.cursor()
            sqlUser = "SELECT Onboard FROM T_Usuarios WHERE Usuario = '"+ _user +"'"
            cursor.execute(sqlUser)
            data = cursor.fetchone()
            if data:
                return data
            else:
                return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def GetNombre(_user):
    try:
        if _user:
            conn=mysql.connect()
            cursor=conn.cursor()
            sqlUser = "SELECT Nombre FROM T_Usuarios WHERE ID_Usuario = '"+_user+"'"
            cursor.execute(sqlUser)
            data = cursor.fetchone()
            if data:
                return data
            else:
                return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()
    

def Id_Usuario(_correo):
    try:
        if _correo:
            conn=mysql.connect()
            cursor=conn.cursor()
            sqlUser = "SELECT ID_Usuario FROM T_Usuarios WHERE Correo = %s"
            cursor.execute(sqlUser,(_correo))
            data = cursor.fetchone()
            if data:
                return data
            else:
                return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def IniciarP(_id):
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        puntos = "INSERT INTO T_Game (ID_User, Puntos) VALUES ( %s ,'10')"
        cursor.execute(puntos,(_id))
        conn.commit()
        if puntos:
            return True
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        conn.close()
        cursor.close()

def Errores(_user,_error,_errorInfo):
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        sql="INSERT INTO Entidad (User, Error, ErrorInfo) VALUES (%s,%s,%s)"
        query=cursor.execute(sql,(_user,_error,_errorInfo))
        conn.commit()
        if query:
            return True
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        conn.close()
        cursor.close()

def buscarU(_user):
    if _user:
        conn=mysql.connect()
        cursor=conn.cursor()
        query="SELECT Nombre FROM T_Usuarios WHERE Usuario = %s"
        try:
            cursor.execute(query,(_user))
            data=cursor.fetchone()
            if data:
                return data
            else:
                return False
        except:
            return redirect(url_for("error404"))
        finally:
            cursor.close()
            conn.close()

def InsertE(_evento,correo,_sexo,_p1,_p2,_p3,_p4,_p5,_contador, _valor, _porcentaje):
    try:
        if _evento and correo and _sexo and _p1 and _p2 and _p3 and _p4 and _contador and _p5:
            conn=mysql.connect()
            cursor=conn.cursor()
            query="INSERT INTO Encuesta (ID_Evento,Correo, ID_Sexo, P1, P2, P3, P4, P5, Estatus,Calificación, Sentimiento, Valor_Sent) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query,(_evento,correo,_sexo,_p1,_p2,_p3,_p4, _p5,'0',_contador,_valor,_porcentaje))
            conn.commit()
            if query:
                return True
            else:
                return False
    except:
        return redirect(url_for("error404"))
    finally:
        conn.close()
        cursor.close()
    

def SelectVer():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _TABLA = "Encuesta"
        query="Select E.ID_Encuesta, V.Nombre as Evento, S.Nombre as Sexo, E.P1, E.P2, E.P3, E.P4, E.P5, E.Calificación, E.Sentimiento FROM Tipo_Encuesta V, Sexo S, Encuesta E WHERE V.ID_Evento = E.ID_Evento and S.ID_Sexo = E.ID_Sexo and E.Estatus ='0'"
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except:
          return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def Sentiment(_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query="select count(*) AS Total, Emotion from T_Images group by Emotion ORDER BY Total DESC"
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except:
          return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()
    

def Image(_id,_event,_name, _emotion):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql_Image = "INSERT INTO T_Images (ID_Evento,ID_Event,Nombre,Emotion) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql_Image,(_id,_event,_name,_emotion))
        conn.commit()
        return "success"
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def ImageSelect(id):
    try:
        #print (id)
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlAll = "SELECT I.Nombre,E.Nombre, I.Emotion FROM T_Images I,T_Eventos E WHERE I.ID_Event= E.ID_Event and E.ID_Evento= %s"
        print(sqlAll)
        cursor.execute(sqlAll,(id))
        data = cursor.fetchall()
        if data:
            return data
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def Eventos(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlEvento = "SELECT E.ID_Event, E.Nombre FROM T_Eventos E, Encuesta Enc WHERE E.ID_Event = Enc.ID_Event AND Enc.ID_Evento = %s"
        cursor.execute(sqlEvento,(id))
        data = cursor.fetchall()
        if data:
            return data
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def Encuestas(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlEvento = "SELECT Enc.ID_Encuesta, Enc.Correo, Enc.Calificación, Enc.Sentimiento,T.ID_Evento, E.Nombre FROM Encuesta Enc, Tipo_Encuesta T, T_Eventos E WHERE Enc.ID_Evento = T.ID_Evento and Enc.ID_Event = E.ID_Event and Enc.ID_Evento= %s"
        cursor.execute(sqlEvento,(id))
        data = cursor.fetchall()
        if data:
            return data
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()
def Preguntas(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlEvento = "SELECT ID_Encuesta,P1,P2,P3,P4,p5 FROM Encuesta WHERE ID_Encuesta =" + id
        cursor.execute(sqlEvento)
        data = cursor.fetchall()
        if data:
            return data
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def SelectAll(_correo):
    try:
        if _correo:
            conn=mysql.connect()
            cursor=conn.cursor()
            sqlUser = "SELECT Rnd FROM T_Usuarios WHERE Correo = %s"
            cursor.execute(sqlUser,(_correo))
            data = cursor.fetchone()
            if data:
                return data
            else:
                return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def UpdateRnd(_correo):
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        query="UPDATE T_Usuarios SET Rnd = '0' WHERE Correo = %s"
        cursor.execute(query,(_correo))
        conn.commit()
        if query:
            return True
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def validarCorreo(correo,rnd):
    try:
        if correo:
            conn=mysql.connect()
            cursor=conn.cursor()
            query="SELECT * FROM T_Usuarios WHERE Correo = %s"
            cursor.execute(query,(correo))
            data=cursor.fetchone()
            if data:
                query1= "UPDATE T_Usuarios SET Rnd = %s WHERE Correo = %s"
                cursor.execute(query1,(rnd,correo))
                conn.commit()
                return True
            else:
                return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def validarUsuario(_user,_password,pass_enc):
    try:
        if _user and _password:
            conn=mysql.connect()
            cursor=conn.cursor()
            query="SELECT * FROM T_Usuarios WHERE Usuario = %s"
            cursor.execute(query,(_user))
            data=cursor.fetchone()
            if data != None:
                pass_encrip_encode= data[5].encode()
                if (bcrypt.checkpw(pass_enc,pass_encrip_encode)):
                    return True
                else:
                    return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def enviarCorreoEnc(mail):
    try:
        if mail:
            conn=mysql.connect()
            cursor=conn.cursor()
            query="SELECT * FROM Encuestas WHERE Correo = %s"
            cursor.execute(query,(mail))
            data=cursor.fetchone()
            if data:
                return True
            else:
                return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def IdUser(user):
    try:
        if user:
            conn=mysql.connect()
            cursor=conn.cursor()
            query="SELECT ID_Usuario FROM T_Usuarios WHERE Nombre = %s"
            cursor.execute(query,(user))
            data=cursor.fetchone()
            if data:
                return data
                #print (data)
            else:
                return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def ConPuntos(con):
    try:
        if con:
            conn=mysql.connect()
            cursor=conn.cursor()
            query="SELECT Puntos FROM T_Game WHERE ID_User = %s"
            cursor.execute(query,(con))
            data=cursor.fetchone()
            if data:
                return data
            else:
                return False
    except:
        return redirect(url_for("error404"))
    finally:
        conn.close()
        cursor.close()

def SumaPuntos(p,con):
    try:
        if p:
            conn=mysql.connect()
            cursor=conn.cursor()
            query="UPDATE T_Game SET Puntos = %s WHERE ID_User = %s"
            cursor.execute(query,(p , con))
            conn.commit()
            if query:
                return True
            else:
                return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def EventosEnc(id):
    try:
        if id:
            conn=mysql.connect()
            cursor=conn.cursor()
            query="SELECT ID_Event, Nombre FROM T_Eventos WHERE ID_Evento = %s"
            cursor.execute(query,(id))
            data=cursor.fetchall()
            if data:
                return data
            else:
                return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def LogOutBoard(name):
    try:
        if name:
            conn=mysql.connect()
            cursor=conn.cursor()
            query="UPDATE T_Usuarios SET Onboard = '1' WHERE Usuario = %s"
            cursor.execute(query,(name))
            conn.commit()
            if query:
                return True
            else:
                return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def SelectOn(name):
    try:
        if name:
            #print(id)
            conn=mysql.connect()
            cursor=conn.cursor()
            query="SELECT Onboard  FROM T_Usuarios WHERE Usuario = %s"
            cursor.execute(query,(name))
            data=cursor.fetchone()
            if data:
                return data
            else:
                return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def SelectCorreos():
    try:
        #print(id)
        conn=mysql.connect()
        cursor=conn.cursor()
        query="SELECT E.Nombre,E.Apellido,E.Correo, E.Fecha,T.Nombre,E.Estatus,E.Sentimiento,E.ID_Prev FROM Tipo_Encuesta T, T_Preventa E WHERE E.ID_Tipo_Ev = T.ID_Evento AND E.Estatus<3"
        cursor.execute(query)
        data=cursor.fetchall()
        if data:
            #print (data)
            return data
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()
    
def InsertPrev(nombre, apellido,correo,fecha,evento,sentiment):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "INSERT INTO T_Preventa (Nombre,Apellido,Correo,Fecha,ID_Tipo_Ev,Estatus, Sentimiento ) VALUES (%s,%s,%s,%s,%s,'0',%s)"
        cursor.execute(sql,(nombre, apellido, correo, fecha, evento, sentiment)) 
        conn.commit()
        return True
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def Select0():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) as Total FROM T_Preventa WHERE Estatus = 0"
        cursor.execute(sql)
        data=cursor.fetchone()
        if data:
            return data
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()
def Select1():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) as Total FROM T_Preventa WHERE Estatus = 1"
        cursor.execute(sql)
        data=cursor.fetchone()
        if data:
            return data
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def Select2():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) as Total FROM T_Preventa WHERE Estatus = 2"
        cursor.execute(sql)
        data=cursor.fetchone()
        if data:
            return data
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def BuscarCorreo2 (correo):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT Estatus FROM T_Preventa WHERE Correo = %s"
        cursor.execute(sql,(correo))
        data=cursor.fetchone()
        if data:
            return data
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def UpdateClient(correo,sentiment,estatus):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "UPDATE T_Preventa SET Sentimiento = %s, Estatus = %s WHERE Correo = %s"
        cursor.execute(sql,(sentiment,estatus,correo))
        conn.commit()
        #data=cursor.fetchone()
        if sql:
            return True
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()


def InsertEnvCorreo(de,para,asunto,body):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "INSERT INTO T_Correos_env (Para, De, Asunto, Body) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(de, para, asunto,body))
        conn.commit()
        #data=cursor.fetchone()
        if sql:
            return True
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def SelectUser(correo):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT ID_Prev FROM T_Preventa WHERE Correo = %s"
        cursor.execute(sql,(correo))
        data=cursor.fetchone()
        if data:
            return data
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def InsertCE(para,de,asunto,body,user):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "INSERT INTO T_Correos_env(Para,De,Asunto,Body,ID_Cliente,ID_Correo_Tipo) VALUES (%s,%s,%s,%s,%s,'1')"
        cursor.execute(sql,(para,de,asunto,body,user)) 
        insert=conn.commit()
        #print (sql)
        if insert:
            return True
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def InsertCR(para,de,asunto,body,fecha,user):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "INSERT INTO T_Correos_env(Para,De,Asunto,Body,Fecha,ID_Cliente,ID_Correo_Tipo) VALUES (%s,%s,%s,%s,%s,%s,'2')"
        cursor.execute(sql,(de,para,asunto,body,fecha,user)) 
        insert=conn.commit()
        #print (sql)
        if insert:
            return True
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def Tracking(correo):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT C.Para, C.De, C.Asunto,C.Body, C.Fecha, U.Correo FROM T_Correos_env C, T_Preventa U WHERE C.ID_Cliente=U.ID_Prev AND U.Correo = %s"
        cursor.execute(sql,(correo))
        data=cursor.fetchall()
        if data:
            return data
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

#Contratos - Querys
def InsertContrato(location,date,Nombre,Nombre2,curp_conyuge1,curp_conyuge2,domicilio2,filename,filename2,filename3):
    try:
        if location and date and Nombre and Nombre2 and curp_conyuge1 and curp_conyuge2 and domicilio2 and filename and filename2 and filename3:
            conn=mysql.connect()
            cursor=conn.cursor()            
            query="INSERT INTO T_Contratos (Nombre1,Nombre2,Curp1,Curp2,Domicilio,Fecha_Evento,Archivo1,Archivo2,Archivo3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            print("Base de Datos22")
            cursor.execute(query,(Nombre,Nombre2,curp_conyuge1,curp_conyuge2,domicilio2,location,date,filename,filename2,filename3))
            conn.commit()
            if query:
                return True
            else:
                return False
    except:
        return print("Error en el insert")
    finally:
        conn.close()
        cursor.close()


def SelectCont(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlEvento = "SELECT ID_Contrato,Nombre1,Nombre2,Curp1,Curp2,Domicilio,Fecha_Evento,Archivo1,Archivo2,Archivo3 FROM T_Contratos WHERE ID_Contrato =" + id
        cursor.execute(sqlEvento)
        data = cursor.fetchall()
        if data:
            return data
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def SelectLugar():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlEvento = "SELECT ID_Lugar, Nombre FROM T_Lugares"
        cursor.execute(sqlEvento)
        data = cursor.fetchall()
        if data:
            return data
        else:
            return False
    except:
        return print("error en el select")
    finally:
        cursor.close()
        conn.close()

def SelectBuscarIDSalon(nombre_salon):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlEvento = "SELECT ID_Lugar FROM T_Lugares WHERE Nombre = %s"
        cursor.execute(sqlEvento,(nombre_salon))
        data = cursor.fetchone()
        if data:
            return data
        else:
            return False
    except:
        return print("error en el select")
    finally:
        cursor.close()
        conn.close()

def SelectId(correo):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlEvento = "SELECT P.ID_Prev, E.Nombre FROM T_Preventa P, Tipo_Encuesta E WHERE P.ID_Tipo_Ev = E.ID_Evento AND P.Correo = %s"
        cursor.execute(sqlEvento,(correo))
        data = cursor.fetchone()
        if data:
            return data
        else:
            return False
    except:
        return print("error en el select")
    finally:
        cursor.close()
        conn.close()

def SelectTipo(correo):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlEvento = "SELECT ID_Prev, ID_Tipo_Ev FROM T_Preventa WHERE Correo = %s"
        cursor.execute(sqlEvento,(correo))
        data = cursor.fetchone()
        if data:
            return data
        else:
            return False
    except:
        return print("error en el select :(:(")
    finally:
        cursor.close()
        conn.close()

def InsertContratoBoda(Nombre,Nombre2,curp_conyuge1,curp_conyuge2,domicilio2,date,id_location,filename,filename2,filename3,id_evento,cliente):
    try:
        if Nombre and Nombre2 and curp_conyuge1 and curp_conyuge2 and domicilio2 and date and id_location and filename and filename2 and filename3 and id_evento and cliente:
            conn=mysql.connect()
            cursor=conn.cursor()            
            query="INSERT INTO T_Contratos (Nombre1,Nombre2,Curp1,Curp2,Domicilio,Fecha_Evento,ID_Lugar,Archivo1,Archivo2,Archivo3,ID_Tipo_Evento,ID_Cliente,ID_Tipo,Estatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,'3','0')"
            cursor.execute(query,(Nombre,Nombre2,curp_conyuge1,curp_conyuge2,domicilio2,date,id_location,filename,filename2,filename3,id_evento,cliente))
            instert = conn.commit()
            if instert:
                return True
            else:
                return False
    except:
        return print("Error en el insert")
    finally:
        conn.close()
        cursor.close() 

def InsertContratoGeneral(Nombre,curp_conyuge1,domicilio2,date,id_location,filename,filename3,id_evento,cliente):
    try:
        if Nombre and curp_conyuge1 and domicilio2 and date and id_location and filename and filename3 and id_evento and cliente:
            conn=mysql.connect()
            cursor=conn.cursor()            
            query="INSERT INTO T_Contratos (Nombre1,Curp1,Domicilio,Fecha_Evento,ID_Lugar,Archivo1,Archivo3,ID_Tipo_Evento,ID_Cliente,ID_Tipo,Estatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,'4','0')"
            cursor.execute(query,(Nombre,curp_conyuge1,domicilio2,date,id_location,filename,filename3,id_evento,cliente))
            instert = conn.commit()
            if instert:
                return True
            else:
                return False
    except:
        return print("Error en el insert")
    finally:
        conn.close()
        cursor.close()

def SelectContratoBodas():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlEvento = "SELECT ID_Contrato,Nombre1 FROM T_Contratos WHERE ID_Tipo_Evento = '3' AND Estatus = '0'"
        cursor.execute(sqlEvento)
        data = cursor.fetchall()
        if data:
            return data
        else:
            return False
    except:
        return print("Error en el select :(")
    finally:
        cursor.close()
        conn.close()
def SelectAllBodas(id_cont):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlEvento = "SELECT C.Nombre1, C.Nombre2, C.Curp1, C.Curp2, C.Domicilio, C.Fecha_Evento, L.Nombre, C.Archivo1, C.Archivo2, C.Archivo3, U.Correo, E.Nombre FROM T_Contratos C, T_Lugares L, Tipo_Encuesta E, T_Preventa U WHERE C.ID_Lugar = L.ID_Lugar AND C.ID_Tipo_Evento = E.ID_Evento AND C.ID_Cliente = U.ID_Prev AND C.ID_Contrato = %s"
        cursor.execute(sqlEvento,(id_cont))
        data = cursor.fetchone()
        print(id_cont)
        print(data)
        if data:
            return data
        else:
            return False
    except:
        return print("Error en el select :(")
    finally:
        cursor.close()
        conn.close()

def SelectAllXV(id_cont):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlEvento = "SELECT C.Nombre1, C.Curp1, C.Domicilio, C.Fecha_Evento, L.Nombre, C.Archivo1, C.Archivo3, U.Correo, E.Nombre FROM T_Contratos C, T_Lugares L, Tipo_Encuesta E, T_Preventa U WHERE C.ID_Lugar = L.ID_Lugar AND C.ID_Tipo_Evento = E.ID_Evento AND C.ID_Cliente = U.ID_Prev AND C.ID_Contrato = %s"
        cursor.execute(sqlEvento,(id_cont))
        data = cursor.fetchone()
        print(id_cont)
        print(data)
        if data:
            return data
        else:
            return False
    except:
        return print("Error en el select :(")
    finally:
        cursor.close()
        conn.close()

def SelectContratoXV():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlEvento = "SELECT ID_Contrato,Nombre1 FROM T_Contratos WHERE ID_Tipo_Evento = '4' AND Estatus = '0'"
        cursor.execute(sqlEvento)
        data = cursor.fetchall()
        if data:
            return data
        else:
            return False
    except:
        return print("Error en el select :(")
    finally:
        cursor.close()
        conn.close()

def SelectContratoTec():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlEvento = "SELECT ID_Contrato,Nombre1 FROM T_Contratos WHERE ID_Tipo_Evento = '5' AND Estatus = '0'"
        cursor.execute(sqlEvento)
        data = cursor.fetchall()
        if data:
            return data
        else:
            return False
    except:
        return print("Error en el select :(")
    finally:
        cursor.close()
        conn.close()


def SelectContratoOtros():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlEvento = "SELECT ID_Contrato,Nombre1 FROM T_Contratos WHERE ID_Tipo_Evento = '6' AND Estatus = '0'"
        cursor.execute(sqlEvento)
        data = cursor.fetchall()
        if data:
            return data
        else:
            return False
    except:
        return print("Error en el select :(")
    finally:
        cursor.close()
        conn.close()

def SelectPuntos(user):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlEvento = "SELECT P.Puntos, U.Usuario, P.ID_User FROM T_Game P, T_Usuarios U WHERE P.ID_User = U.ID_Usuario AND U.Usuario = %s"
        print(sqlEvento)
        cursor.execute(sqlEvento,(user))
        data = cursor.fetchone()
        if data:
            return data
        else:
            return False
    except:
        return print("Error en el select :(")
    finally:
        cursor.close()
        conn.close()

def InsertPuntos(puntos, id_user):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "UPDATE T_Game SET Puntos = %s WHERE ID_User = %s"
        cursor.execute(sql,(puntos,id_user)) 
        insert=conn.commit()
        #print (sql)
        if insert:
            return True
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()

def UpdateEstatus (id):
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        query="UPDATE T_Contratos SET Estatus = '1' WHERE ID_Contrato = %s"
        cursor.execute(query,(id))
        conn.commit()
        if query:
            return True
        else:
            return False
    except:
        return redirect(url_for("error404"))
    finally:
        cursor.close()
        conn.close()
