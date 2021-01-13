#Flask Libraries
from flask import Flask, json, render_template, request, g, redirect, session, url_for, jsonify, flash, make_response
import requests
from datetime import timedelta
from flask_wtf import FlaskForm
from wtforms import FileField
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename 
from flask_mail import Mail
from flask_mail import Message
from werkzeug.security import generate_password_hash 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
from email.message import EmailMessage
from smtplib import SMTP
from selenium  import webdriver
import modelo as modelo
import service as service
import facei as facei
import getpass, poplib 
from email.parser import Parser
import imaplib 
import email 
from email.header import decode_header
import os
import bcrypt
from random import randint
import time
import re

#contratos
import pdfkit

#Import Azure Libraries
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
#from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from flask_uploads import configure_uploads, IMAGES, UploadSet


UPLOAD_FOLDER = os.path.abspath(r"E:/Documents/Programacion/Python/Work&Party/venv/static/upload")
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])

config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")

#config = pdfkit.configuration(wkhtmltopdf="./bin/wkhtmltopdf") 
#Config para heroku

app = Flask(__name__)
app.secret_key = "TH1S1STH3PR0Y3CT"
app.config['SESSION_TYPE']='filesystem'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

#Contratos Global Variables
UPLOAD_FOLDER_CONTRATOS = os.path.abspath("static/upload/img")
app.config['UPLOADED_IMAGES_DEST'] = UPLOAD_FOLDER_CONTRATOS
subscription_key = "69432c0e60ea4cba9d3875f7edfefe44"
endpoint = "https://vi-tech-computer-vision.cognitiveservices.azure.com/"
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
class MyForm(FlaskForm):
    image = FileField('image')
    image2 = FileField('image')
    image3 = FileField('image')

images = UploadSet('images',IMAGES)

configure_uploads(app,images)

#config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files (x86)/wkhtmltopdf/bin/wkhtmltopdf.exe") 

#config = pdfkit.configuration(wkhtmltopdf="./bin/wkhtmltopdf") 
#Config para heroku


salt=bcrypt.gensalt()

#app.permanent_session_lifetime=timedelta(minutes=5)

@app.before_request
def before_request():
    g.user = None   
    if 'user' in session:
        g.user = modelo.buscarU(session['user'])
        

@app.route('/')
def home():
    return redirect(url_for("login"))

@app.route('/blog', methods=['POST','GET'])
def blog():
    if request.method == 'POST':
        datos = request.get_json()
        print(datos)
        nombre = datos['nombre']
        apellido = datos['apellido']
        fecha= datos['fecha']
        correo = datos['correo']
        asunto = datos['asunto']
        evento = datos['evento']
        consulta = service.Texto(asunto)
        sentiment = consulta['documents'][0]['sentiment']
        insert = modelo.InsertPrev(nombre,apellido,correo,fecha,evento,sentiment)
        if insert:
            resJSON = { "alerta" : "Si"}
            print("insertado")
        else:
            resJSON = { "alerta" : "En algo fallamos"}
            print("fallo")
        return jsonify(resJSON)
    return render_template("indexblog.html")

@app.route('/inicioBlog')
def inicioBlog():
    return render_template("iniciob.html")

@app.route('/registrar',methods=['POST','GET'])
def registrar():
    if request.method == 'POST':
        nombre = request.form['name']
        apellido = request.form['last_name']
        correo = request.form['email']
        print (correo)
        contra = request.form['password']
        contra2 = request.form['password2']
        user = request.form['usuario']
        if contra == contra2:
            password_encode= contra.encode("utf-8")
            password_encrip=bcrypt.hashpw(password_encode,salt)
        add = modelo.InsertUser(nombre,apellido,correo,password_encrip,user)
        if add:
            u = modelo.Id_Usuario(correo)
            print (modelo.IniciarP(u))
            flash("Cuenta creada exitosamente")
            modelo.Errores(correo,"Registro.Sucess","Se logró registrar el usuario")
            print("redirigimos")
            return render_template('login.html')
        else:
            modelo.Errores(correo,"Registro.Fail","No se logró registrar el usuario")
            return render_template('registrar.html')
    return render_template ("registrar.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('inicio'))
    if request.method == 'POST':
        _user = request.form['user']
        _password = request.form['pass']
        _password_enc= _password.encode ("utf-8")
        if (_user and _password):
            usuario = modelo.validarUsuario(_user,_password,_password_enc)
            if usuario == True:
                session["user"] = _user
                modelo.Errores(_user,'Login.Sucess','Se logra el login')
                return redirect(url_for('set_cookie', user = _user))
            else:
                flash("Datos erroneos, verifique de nuevo.")
                modelo.Errores(_user,'Login.Fail','Datos erroneos')
                return render_template('login.html')
    return render_template("login.html")

#Cookie para conteo de contratos generados
@app.route('/set_cookie')
def set_cookie():

    cookie_contratos = '0'

    response = make_response(redirect(url_for('inicio')))

    response.set_cookie('badges',cookie_contratos)

    return response

@app.route('/delete_cookie')
def delete_cookie():

    response = make_response(redirect(url_for('login')))

    response.set_cookie('badges', '', expires=0)

    return response

@app.route('/recupera', methods=['POST','GET'])
def olvide():
    if request.method == 'POST':
        mail= request.form['correo']
        lista = []
        for x in range(8):
            a = randint(0,9)
            lista.append(str(a)) #Estas 2 líneas se pueden juntar en: lista.append(str(randint(0,9))
        valor = ''
        for x in range(8):
            valor = valor + lista[x]
        #print (valor)
        snd=modelo.validarCorreo(mail,valor)
        if snd:
            s= smtplib.SMTP(host='smtp.gmail.com',port=587)
            s.starttls()
            s.login('dreamteamdsc@gmail.com','Desarrollo7')

            msg= EmailMessage()
            msg.set_content(f"""
                                Hemos recibido tu solicitud para restablecer tu contraseña, te enviamos un código de validación {valor} </br>
                                De igual manera te dejamos el siguiente enlace para que realices el cambio
                                """)
            #msg.set_content(html)
            msg['Subject']='Restablecer contraseña'
            msg['From']='dreamteamdsc@gmail.com'
            msg['To']=mail

            s.send_message(msg)
            s.quit()
            modelo.Errores(mail,'MailPass.Success','Se logra el envio de mail para recuperación de contraseña')
            return "Email sent"
        else:
            modelo.Errores(mail,'MailPass.Fail','No se logra el envio de mail para recuperación de contraseña')
            return render_template("404.html")
    return render_template('olvide.html')

@app.route('/cambiar', methods=['POST', 'GET'])
def cambiar():
    if request.method == 'POST':
        mail= request.form['correo']
        contra= request.form['contra']
        contra1=request.form['contra1']
        code = request.form['codigo']
        if contra == contra1:
            _password_enc= contra.encode ("utf-8")
            bcrypt.hashpw(_password_enc,salt)
            usuario = modelo.SelectAll(mail)
            if usuario[0] == int(code):
                snd = modelo.UpdateRnd(mail)
                if snd:
                    print('Actualizado')
                    modelo.Errores(mail,"ChangePass.Success",'Se logra el cambio de contraseña')
                else:
                    print('No actualizo')
                    modelo.Errores(mail,'ChangePass.Fail','No se logra el cambio de contraseña')
    return render_template('restablecer.html')

@app.route('/inicio', methods=['GET','POST'])
def inicio():
    if 'user' in session:
        user=session['user']
        if request.method == 'POST':
            _asunto = request.form['asunto']
            _de = request.form['de']
            _para = "encuestasoporte0@gmail.com"
        puntos = modelo.SelectPuntos(user)
        print(puntos)
        if puntos:
            puntos2 = puntos[0]
            print(puntos2)
        else:
            print("No hay puntos para ti")


        return render_template("index.html", puntos = puntos2)
    return render_template("login.html")

@app.route('/obtenerpuntos',methods=['GET','POST'])
def obtenerpuntos():
    if 'user' in session:
        user=session['user']
        if request.method=='POST':
            datos = request.get_json()
            obtener = datos['obtener']
            print(obtener)
            puntos = modelo.SelectPuntos(user)
            if puntos:
                puntos2 = puntos[0]
                print(puntos2)
                resJSON = {"alerta" : "Si", "puntos": puntos2}
                return jsonify(resJSON)


@app.route('/eventosBoda',methods=['GET','POST'])
def eventosBoda():
    if 'user' in session:
        user = session['user']
        id = 3
        if request.method == "POST":
            f = request.files["ourfile"]
            e = request.form["evento"]
            filename = f.filename
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            emotion = facei.Images(filename)
            if emotion:
                im = modelo.Image(id,e,filename, emotion)
                if im:
                    modelo.Errores(user,'ImageLoad.Sucess','Se carga la imagen')
                    return redirect(url_for('eventosBoda'))
                else:
                   modelo.Errores(user,'ImageLoad.Fail','No se carga la imagen')
                   return redirect(url_for('error404'))
        sentiments = modelo.Sentiment(id)
        imagenes = modelo.ImageSelect(id)
        eventos = modelo.Eventos(id)
        encuestas = modelo.Encuestas(id)
        id_encuesta = encuestas[0]
        #onboarding = modelo.Onboarding(user)
        if eventos:
            return render_template("eventos.html", eventos = eventos, encuestas = encuestas, imagenes = imagenes, sentiments = sentiments, id_encuesta = id_encuesta)
        else:
            return redirect(url_for("inicio"))
    else:
        return redirect(url_for("inicio"))

@app.route('/eventosXv',methods=['GET','POST'])
def eventosXv():
    if 'user' in session:
        user = session['user']
        id = 4
        if request.method == "POST":
            print('holi if post')
            f = request.files["ourfile"]
            e = request.form["evento"]
            filename = f.filename
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            emotion = facei.Images(filename)
            if emotion:
                im = modelo.Image(id,e,filename, emotion)
                if im:
                    modelo.Errores(user,'ImageLoad.Sucess','Se carga la imagen')
                    return redirect(url_for('eventosXv'))
                else:
                    modelo.Errores(user,'ImageLoad.Fail','No se carga la imagen')
                    return redirect(url_for('error404'))
        sentiments = modelo.Sentiment(id)
        imagenes = modelo.ImageSelect(id)
        eventos = modelo.Eventos(id)
        encuestas = modelo.Encuestas(id)
        id_encuesta = encuestas[0]
        #onboarding = modelo.Onboarding(user)
        if eventos:
            return render_template("eventos.html", eventos = eventos, encuestas = encuestas, imagenes = imagenes, sentiments = sentiments, id_encuesta = id_encuesta)
        else:
            return redirect(url_for("inicio"))
    else:
        return redirect(url_for("inicio"))


@app.route('/eventosTec',methods=['GET','POST'])
def eventosTec():
    if 'user' in session:
        user = session['user']
        id = 5
        if request.method == "POST":
            print('se hizo un post')
            f = request.files["ourfile"]
            e = request.form["evento"]
            filename = f.filename
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            emotion = facei.Images(filename)
            if emotion:
                im = modelo.Image(id,e,filename, emotion)
                if im:
                    modelo.Errores(user,'ImageLoad.Sucess','Se carga la imagen')
                    return redirect(url_for('eventosTec'))
                else:
                   modelo.Errores(user,'ImageLoad.Fail','No se carga la imagen')
                   return redirect(url_for('error404'))
        print(id)
        sentiments = modelo.Sentiment(id)
        print(sentiments)
        imagenes = modelo.ImageSelect(id)
        print(imagenes)
        eventos = modelo.Eventos(id)
        print(eventos)
        encuestas = modelo.Encuestas(id)
        print(encuestas)
        id_encuesta = encuestas[0]
        #onboarding = modelo.Onboarding(user)
        if eventos:
            return render_template("eventos.html", eventos = eventos, encuestas = encuestas, imagenes = imagenes, sentiments = sentiments, id_encuesta = id_encuesta)
        else:
            return redirect(url_for("inicio"))
    else:
        return redirect(url_for("inicio"))

@app.route('/eventosOtro',methods=['GET','POST'])
def eventosOtro():
    if 'user' in session:
        user = session['user']
        id = 6
        if request.method == "POST":
            f = request.files["ourfile"]
            e = request.form["evento"]
            filename = f.filename
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            emotion = facei.Images(filename)
            if emotion:
                im = modelo.Image(id,e,filename, emotion)
                if im:
                    modelo.Errores(user,'ImageLoad.Sucess','Se carga la imagen')
                    return redirect(url_for('eventosOtro'))
                else:
                    modelo.Errores(user,'ImageLoad.Fail','No se carga la imagen')
                    return redirect(url_for('error404'))
        sentiments = modelo.Sentiment(id)
        imagenes = modelo.ImageSelect(id)
        eventos = modelo.Eventos(id)
        encuestas = modelo.Encuestas(id)
        id_encuesta = encuestas[0]
        #onboarding = modelo.Onboarding(user)
        if eventos:
            return render_template("eventos.html", eventos = eventos, encuestas = encuestas, imagenes = imagenes, sentiments = sentiments, id_encuesta = id_encuesta)
        else:
            return redirect(url_for("inicio"))
    else:
        return redirect(url_for("inicio"))


@app.route('/detalles', methods = ['GET', 'POST'])
def detalles():
    if request.method == 'POST':
        datos = request.get_json()
        detalle = modelo.Preguntas(datos['Id'])
        resJSON = { 
            "alerta" : "Si",
            "p1" : detalle[0][1],            
            "p2" : detalle[0][2],
            "p3" : detalle[0][3],
            "p4" : detalle[0][4],
            "p5" : detalle[0][5]
        }
        return jsonify(resJSON)

@app.route('/opinion', methods=['GET','POST'])
def opinion():
    if request.method == 'POST':
        print("Enviado")
    return render_template('opinion.html')

@app.route('/gracias', methods = ['POST', 'GET'])
def gracias():
    if request.method == 'POST':
        correo=request.form['correo']
        evento=request.form['evento']
        sexo = request.form['sexo']
        p1 = request.form['ans']
        p2 = request.form['p2']
        p3 = request.form['p3']
        p4 = request.form['p4'] 
        p5= request.form['p5'] 
        consulta = service.Texto(p5)
        valor = consulta['documents'][0]['sentiment']
        if valor == 'positive':
            porcentaje = consulta['documents'][0]['confidenceScores']['positive']
        elif valor == 'negative':
            porcentaje = consulta['documents'][0]['confidenceScores']['negative']
        else:
            porcentaje = consulta['documents'][0]['confidenceScores']['neutral']
        r = []
        contador = 0
        r.append(p1)
        r.append(p2)
        r.append(p3)
        r.append(p4)
        r.append(valor)
        for cal in r:
            if cal == 'Si':
                contador += 1
            if cal == 'Bueno':
                contador += .75
            if cal == 'Regular':
                contador += .50
            if cal == 'Malo':
                contador += .25
            if cal == 'No':
                contador += 0
            if cal == 'Excelente':
                contador += 1
            if cal == "positive":
                contador += 1
            if cal == "neutral":
                contador += .50
            if cal == "negative":
                contador += .25
        modelo.InsertE(evento,correo,sexo,p1,p2,p3,p4,p5,contador,valor,porcentaje)
    return render_template('opinion.html')

@app.route('/logout')
def logout():
    user=session['user']
    snd=modelo.SelectOn(user)
    if snd[0] == 0:
        modelo.LogOutBoard(user)
        session.pop("user", None)
    else:
        session.pop("user", None)
    return redirect(url_for("delete_cookie"))

@app.route("/error404")
def error404():
    return render_template("404.html")

@app.route("/enviar",methods=['POST','GET'])
def enviar():
    if 'user' in session:
        if request.method == "POST":
            datos = request.get_json()
            print(datos)
            correo = datos['Correo']
            cal = datos['Cal']
            user=session['user']
            snd=modelo.enviarCorreoEnc(correo)
            modelo.IdUser(user)
            if snd:
                mailServer = smtplib.SMTP('smtp.gmail.com',587)
                mailServer.ehlo()
                mailServer.starttls()
                mailServer.ehlo()
                mailServer.login('dreamteamdsc@gmail.com','Desarrollo7')
                if float(cal) > 2.5:
                    #Construimos el mensaje simple
                    mensaje = MIMEText("""Nos encanta que tengas un buen evento con nosotros, puedes ir a nuestra pagina donde puedes dejarnos un comentario donde nos puedes ayudar a mejorar :) te esperamos de vuelta http://127.0.0.1:5000/blog """)
                    mensaje['From']="dreamteamdsc@gmail.com"
                    mensaje['To']=correo
                    mensaje['Subject']="Tienes un correo"
                    #Envio del mensaje
                    mailServer.sendmail("dreamteamdsc@gmail.com", correo, mensaje.as_string())
                    mailServer.close()
                    resJSON = { "alerta" : "Si"}
                    return jsonify(resJSON)
                if float(cal) < 2.5:
                    #Construimos el mensaje simple
                    mensaje = MIMEText("""Lamentamos que hayas tenido un mal evento con nosotros :(, la opimos de nuestros clientes es muy importante para nosotros, puedes ir a nuestra pagina donde puedes dejarnos un comentario donde nos puedes ayudar a mejorar :) te esperamos de vuelta
                    http://127.0.0.1:5000/blog """)
                    mensaje['From']="dreamteamdsc@gmail.com"
                    mensaje['To']=correo
                    mensaje['Subject']="Tienes un correo"
                    #Envio del mensaje
                    mailServer.sendmail("dreamteamdsc@gmail.com", correo, mensaje.as_string())
                    mailServer.close()
                    resJSON = { "alerta" : "Si"}
                    return jsonify(resJSON)
                
    else:
        return redirect(url_for('login'))

@app.route('/preventa')
def preventa():
    if 'user' in session:
        user = session['user']
        print(user)
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('dreamteamdsc@gmail.com','Desarrollo7')
        mail.select ('inbox') 
        _, search_data = mail.search(None, 'UNSEEN')
        my_message = []
        for num in search_data[0].split():
            email_data = {}
            _, data = mail.fetch(num, '(RFC822)')
            _, b = data[0]
            email_message = email.message_from_bytes(b)
            for header in ['subject', 'to', 'from', 'date']:
                email_data[header] = email_message[header]
                print("Header----")
                print (email_data)
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode()
                    fecha=email_data['date']
                    array_of_date = fecha.split(" ")
                    dia = array_of_date[1]
                    hora = array_of_date[4]
                    nfecha = "2020-12-" + dia + " " + hora
                    print(nfecha)
                    asunto=email_data['subject']
                    print (asunto)
                    de = email_data['from']
                    s2 = email_data['to'].replace(">","").split("<")
                    try:
                        para = s2[1]
                    except:
                        para = 'dreamteamdsc@gmail.com'
                    print (para)
                elif part.get_content_type() == "text/html":
                    html_body = part.get_payload(decode=True)
                    email_data['html_body'] = html_body.decode()
            my_message.append(email_data)
            s1 = email_data['from'].replace(">","").split("<")
            correo = s1[1]
            b1 = email_data['body'].split("El")
            body = b1[0].strip()         
            print(correo,"-",body)
            con = modelo.BuscarCorreo2(correo)
            print (con)
            if con:
                if int(con[0]) != 3:
                    N_estatus = int(con[0]) + 1
                    consulta = service.Texto(body)
                    sentiment = consulta['documents'][0]['sentiment']
                    modelo.UpdateClient(correo, sentiment, N_estatus)
                    user = modelo.SelectUser(correo)
                    print(user)
                    print(sentiment)
                    user2= user[0]
                    if user:
                        insert = modelo.InsertCR(correo,para,asunto,body,nfecha,user2)
                        print (insert)
                        if insert:
                            print("Se logró insertar el correo")
                        else:
                            print("No se logró insertar el correo")                            
                    else:
                        print("No existe esa preventa")

        # Select de Correos para llenar la tabla de nuevo
        correos = modelo.SelectCorreos()
        S0 = modelo.Select0()
        S1 = modelo.Select1()
        S2 = modelo.Select2()
        return render_template("preventa.html", correos = correos, S0 = S0, S1 = S1, S2 = S2)
    else:
        return redirect(url_for("login"))

@app.route('/eprev', methods = ["POST", "GET"])
def eprev():
    if 'user' in session:
        user = session['user']
    if request.method == "POST":
        datos = request.get_json()
        print(datos)
        de="dreamteamdsc@gmail.com"
        Correo = datos['Correo']
        Cuerpo = datos['Cuerpo']
        Asunto = datos['Asunto']
        Tipo = datos['Tipo']
        html=None
        print(Correo)
        print(Cuerpo)
        print(Asunto)
        mailServer = smtplib.SMTP('smtp.gmail.com',587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login('dreamteamdsc@gmail.com','Desarrollo7')
        #------------------------------------------ 
        mensaje=MIMEMultipart('alternative')
        mensaje['From']="dreamteamdsc@gmail.com"
        mensaje['To']=Correo
        mensaje['Subject']="Tienes un correo"
        txt_part = MIMEText(Cuerpo,'plain')
        mensaje.attach(txt_part)
        if html != None:
            html_part=MIMEText(html,'html')
            mensaje.attach(html_part)
        msn_str=mensaje.as_string()
      
        #Envio del mensaje
        mailServer.sendmail("dreamteamdsc@gmail.com", Correo, msn_str.encode('utf-8'))
        user=modelo.SelectUser(Correo)
        user2=user[0]
        if user2:
            insert=modelo.InsertCE(Correo,de,Asunto,Cuerpo,user2)
            if insert:
                print("Insertado")
                selectpuntos=modelo.SelectPuntos(user)
                print(selectpuntos)
            else:
                print("No se logró insertar")
        mailServer.close()
        resJSON = { "alerta" : "Si"}
        return jsonify(resJSON)
    return redirect(url_for('preventa'))

@app.route('/points',methods=['POST','GET'])
def points():
    if request.method=='POST':
        print("POINTS")
        if 'user' in session:
            user = session['user']
            print(user)
            datos=request.get_json()
            try:
                puntos = modelo.SelectPuntos(user)
                if puntos:
                    points = int(puntos[0]) + 5
                    id_user=puntos[2]
                    print(points)
                    print(id_user)
                    insert = modelo.InsertPuntos(points,id_user)
                    print(insert)
                    if insert:
                        print("Se actualizo")
                    else:
                        print("No se actualizo pero si se actualiza")
                resJSON={'alerta':'Si'}
            except:
                resJSON={'alerta':'No'}                    
        return jsonify(resJSON)


@app.route('/tracking', methods = ["POST", "GET"])
def tracking():
    datos = request.get_json()
    correo = datos['Correo']
    try:
        tracking = modelo.Tracking(correo)
        de = []
        body = []
        fecha = []
        for correo in tracking:
            de.append(correo[1])
            body.append(correo[3])
            fecha.append(correo[4])
            resJSON = {
                "alerta" : "Si",
                "de": de,
                "body": body,
                "fecha": fecha
                }
        return jsonify(resJSON)
    except:
        resJSON = { "alerta" : "No" }
        return jsonify(resJSON)

@app.route('/landing')
def landing():
    return render_template("landing_evento.html")

#Mis Medallas
@app.route('/badges')
def badges():
    return render_template('badges.html')



#--- CONTRATOS ---

#Contratos - Tablas
@app.route('/contratosBoda', methods = ['POST','GET'])
def contratosBoda():
    SelectContrato = modelo.SelectContratoBodas()
    print(SelectContrato)
    if request.method == "POST":
        datos = request.get_json()
        id_contrato = datos["ID"]
        info_contrato = modelo.SelectAllBodas(id_contrato)
        print(info_contrato)
        nombre = info_contrato[0]
        nombre2 = info_contrato[1]
        curp1 = info_contrato[2]
        curp2 = info_contrato[3]
        domicilio = info_contrato[4]
        date = info_contrato[5]
        location = info_contrato[6]
        filename = info_contrato[7]
        filename2 = info_contrato[8]
        filename3 = info_contrato[9]
        correo = info_contrato[10]
        evento = info_contrato[11]
        print(nombre,nombre2,curp1,curp2,domicilio,date,location,filename,filename2,filename3,correo,evento)
        resJSON={"alerta":"Si", "nombre": nombre, "nombre2": nombre2, "curp1": curp1, "curp2":curp2,"domicilio":domicilio,"date":date,"location":location,"filename":filename,"filename2":filename2,"filename3":filename3,"correo":correo,"evento":evento}
        print(resJSON)
        return jsonify(resJSON)

    return render_template('mis_contratos_boda.html', SelectContrato = SelectContrato)

@app.route('/contratoVerficar',methods=['POST', 'GET'])
def contratoVerificar():
    if request.method == 'POST':
        print()
        datos = request.get_json()
        id = datos['ID']
        print(id)
        update= modelo.UpdateEstatus(id)
        if update:
            print("Se logró actualizar")
        resJSON={"alerta":"Si"}
        return jsonify(resJSON)


@app.route('/contratosXV')
def contratosXV():
    SelectContrato = modelo.SelectContratoXV()
    print(SelectContrato)
    EventoXV = True
    return render_template('mis_contratos_general.html',SelectContrato = SelectContrato, EventoXV = EventoXV)


@app.route('/contratosTec')
def contratosTec():
    SelectContrato = modelo.SelectContratoTec()
    print(SelectContrato)
    EventoTec = True
    return render_template('mis_contratos_general.html',SelectContrato = SelectContrato,EventoTec=EventoTec)

@app.route('/contratosOtros')
def contratosOtros():
    SelectContrato = modelo.SelectContratoOtros()
    print(SelectContrato)
    EventoOtro = True
    return render_template('mis_contratos_general.html',SelectContrato = SelectContrato, EventoOtro = EventoOtro)


#Servicio Cognitivo --- Contratos --- Form para correo
@app.route('/crea_tu_contrato_bodas', methods=['GET','POST'])
def crea_tu_contrato_bodas():
    lugar_salon = modelo.SelectLugar()
    form = MyForm()
    location = "None"
    date="None"
    correo = "None"
    error_ine = "El Archivo Seleccionado NO es una INE :-("
    error_correo = "CORREO NO VALIDO"
    bandera_error = False
    if form.validate_on_submit():
        location = request.form["lc"]
        date = request.form["date"]
        correo = request.form["email"]
        ValidarCorreo = modelo.SelectId(correo)
        if ValidarCorreo:
            print(form.image.data)
            print(form.image2.data)
            print(form.image3.data)
            filename = images.save(form.image.data)
            filename2 = images.save(form.image2.data)
            filename3 = images.save(form.image3.data)
            print(f'./static/upload/img/{filename}')
            print(f'./static/upload/img/{filename2}')
            print(f'./static/upload/img/{filename3}')
            print(location)
            print(date)
            ##INE 1
            image = open(f'./static/upload/img/{filename}','rb')
            #image = 'https://i.ibb.co/0rW9ZBv/20201122-182930.jpg'
            #recognize_handw_results = computervision_client.read(_url,language="es", raw=True)
            try:    
                recognize_handw_results = computervision_client.batch_read_file_in_stream(image,raw = True)
            except:
                print("No es una ine")
                return render_template('crea_tu_contrato_bodas.html',form=form,Error = error,error=error,lugar_salon=lugar_salon)
            image.close()
            operation_location_remote = recognize_handw_results.headers["Operation-Location"]
            operation_id = operation_location_remote.split("/")[-1]
            while True:            
                get_handw_text_results = computervision_client.get_read_operation_result(operation_id)
                if get_handw_text_results.status not in ['NotStarted', 'Running']:
                    break
                time.sleep(1)
                contador= ' '
            if get_handw_text_results.status == TextOperationStatusCodes.succeeded:
                for var in get_handw_text_results.recognition_results:
                    for linea in var.lines:
                        #print(linea.text)
                        contador=contador+ '\n' +linea.text
                        #print(" ") 
            
            print(contador)
            #hasta aqui me leyo la ine bien
            #import re
            bandera=""
            bandera = (r"INSTITUTO NACIONAL ELECTORAL\n"
            r"([a-zA-Z0-9]+.+)")
            bandera = re.findall(bandera, contador, re.MULTILINE)
            if len(bandera) >0:
                print("Si es una INE")
                if len(bandera) >0:
                    regex = (r"FECHA DE NACIMIENTO\n"
                    r"(\w+)\n"
                    r"(\d{2}/\d{2}/\d{4})\n"
                    r"(\w+)\n"
                    r"SEXO H\n"
                    r"([a-zA-Z0-9]+.+)\n")

                    domicilio = (r"DOMICILIO\n"
                    r"([a-zA-Z0-9]+.+)\n"
                    r"([a-zA-Z0-9]+.+)\n"
                    r"([a-zA-Z0-9]+.+)\n")

                    curp = (r"CURP ([a-zA-Z0-9]+.+)\n")

                    ApellidoPat = (r"FECHA DE NACIMIENTO\n"
                    r"(\w+)")

                    ApellidoPat = re.findall(ApellidoPat, contador, re.MULTILINE)
                    curp = re.findall(curp, contador, re.MULTILINE)
                    matches = re.findall(regex, contador, re.MULTILINE)
                    domicilio = re.findall(domicilio, contador, re.MULTILINE)
                    
                    

                    print(domicilio)
                    print(ApellidoPat)
                    print(matches)
                    print(curp)

                    try:
                        fecha=matches[0][1]
                        fecha2=fecha[6:10]+"-"+fecha[3:5]+"-"+fecha[0:2]
                    except:
                        fecha = "Hubo un error al Leer, Por Favor, Escribalo Manualmente"
                        fecha2 = "Hubo un error al Leer, Por Favor, Escribalo Manualmente" 
                    try:                   
                        domicilio2=domicilio[0][0]
                        domicilio2=domicilio2+ " " +domicilio[0][1]
                    except:
                        domicilio2 = "Hubo un error al Leer, Por Favor, Escribalo Manualmente"
                    try:
                        curp_conyuge1=curp[0]
                    except:
                        curp_conyuge1 = "Hubo un error al Leer, Por Favor, Escribalo Manualmente"
                    try:
                        Nombre=matches[0][0]+" "+matches[0][2]+" "+matches[0][3]
                    except:
                        Nombre = "Hubo un error al Leer, Por Favor, Escribalo Manualmente"

                    print("este es tu nombre: "+ Nombre)
                    print("este es tu curp: "+ curp_conyuge1)
                    print("este es tu domicilio: " + domicilio2)
                    #Hasta aqui leyo el nombre y el curp, el domicilio no jala
            ##INE 2
            image = open(f'./static/upload/img/{filename2}','rb')
            #image = 'https://i.ibb.co/0rW9ZBv/20201122-182930.jpg'
            #recognize_handw_results = computervision_client.read(_url,language="es", raw=True)    
            try:    
                recognize_handw_results = computervision_client.batch_read_file_in_stream(image,raw = True)
            except:
                print("No es una ine")
                return render_template('crea_tu_contrato_bodas.html',form=form,Error = error,error=error,lugar_salon=lugar_salon)
            image.close()
            operation_location_remote = recognize_handw_results.headers["Operation-Location"]
            operation_id = operation_location_remote.split("/")[-1]
            while True:            
                get_handw_text_results = computervision_client.get_read_operation_result(operation_id)
                if get_handw_text_results.status not in ['NotStarted', 'Running']:
                    break
                time.sleep(1)
                contador= ' '
            if get_handw_text_results.status == TextOperationStatusCodes.succeeded:
                for var in get_handw_text_results.recognition_results:
                    for linea in var.lines:
                        #print(linea.text)
                        contador=contador+ '\n' +linea.text
                        #print(" ") 
            
            print(contador)
            #hasta aqui me leyo la ine bien
            #import re
            bandera=""
            bandera = (r"INSTITUTO NACIONAL ELECTORAL\n"
            r"([a-zA-Z0-9]+.+)")
            bandera = re.findall(bandera, contador, re.MULTILINE)
            if len(bandera) >0:
                print("Si es una INE")
                if len(bandera) >0:
                    regex = (r"FECHA DE NACIMIENTO\n"
                    r"(\w+)\n"
                    r"(\d{2}/\d{2}/\d{4})\n"
                    r"(\w+)\n"
                    r"SEXO M\n"
                    r"([a-zA-Z0-9]+.+)\n")

                    domicilio = (r"DOMICILIO\n"
                    r"([a-zA-Z0-9]+.+)\n"
                    r"([a-zA-Z0-9]+.+)\n"
                    r"([a-zA-Z0-9]+.+)\n")

                    curp = (r"CURP ([a-zA-Z0-9]+.+)\n")

                    ApellidoPat = (r"FECHA DE NACIMIENTO\n"
                    r"(\w+)")

                    ApellidoPat = re.findall(ApellidoPat, contador, re.MULTILINE)
                    curp = re.findall(curp, contador, re.MULTILINE)
                    matches = re.findall(regex, contador, re.MULTILINE)
                    domicilio = re.findall(domicilio, contador, re.MULTILINE)
                    

                    print(domicilio)
                    print(ApellidoPat)
                    print(matches)
                    print(curp)

                    try:
                        fecha=matches[0][1]
                        fecha2=fecha[6:10]+"-"+fecha[3:5]+"-"+fecha[0:2]
                    except:
                        fecha = "Hubo un error al Leer, Por Favor, Escribalo Manualmente"
                        fecha2 = "Hubo un error al Leer, Por Favor, Escribalo Manualmente"
                    try:                    
                        curp_conyuge2=curp[0]
                    except:
                        curp_conyuge2 = "Hubo un error al Leer, Por Favor, Escribalo Manualmente"
                    try:
                        Nombre2=matches[0][0]+" "+matches[0][2]+" "+matches[0][3]
                    except:                 
                        Nombre2 = "Hubo un error al Leer, Por Favor, Escribalo Manualmente"

                    print("este es tu nombre: "+ Nombre2)
                    print("este es tu curp: "+ curp_conyuge2)
                    
                    #return pdf_template_bodas_crea_tu_contrato(location,date,Nombre,Nombre2,curp_conyuge1,curp_conyuge2,domicilio2,filename,filename2,filename3)
                    return crea_tu_contrato_preview(location,date,Nombre,Nombre2,curp_conyuge1,curp_conyuge2,domicilio2,filename,filename2,filename3,correo)
                else:
                    return render_template('crea_tu_contrato_bodas.html',form=form,bandera=True,error=error_ine,lugar_salon=lugar_salon)
            else:
                return render_template('crea_tu_contrato_bodas.html',form=form,bandera=True,error=error_ine,lugar_salon=lugar_salon)
        else:
            return render_template('crea_tu_contrato_bodas.html',form=form,bandera=True,error=error_correo,lugar_salon=lugar_salon)
    return render_template('crea_tu_contrato_bodas.html',form=form,lugar_salon=lugar_salon)

#VISTA PREVIA BODAS
@app.route('/crea_tu_contrato_preview', methods=["POST","GET"])
def crea_tu_contrato_preview(location,date,Nombre,Nombre2,curp_conyuge1,curp_conyuge2,domicilio2,filename,filename2,filename3,correo):
    location = location
    id_salon = modelo.SelectBuscarIDSalon(location)
    id_salon2 = id_salon[0]
    correo = correo
    ValidarCorreo = modelo.SelectId(correo)
    evento = ValidarCorreo[1]
    print(id_salon)
    return render_template('crea_tu_contrato_preview.html', location=location,date=date,Nombre=Nombre,Nombre2=Nombre2,curp_conyuge1=curp_conyuge1,curp_conyuge2=curp_conyuge2,domicilio2=domicilio2,filename=filename,filename2=filename2,filename3=filename3,correo=correo,evento=evento)

#DEBUG BODAS FORM

@app.route('/confirmacion_de_contrato_bodas', methods=["POST","GET"])
def confirmacion_de_contrato_bodas():
    location= "Mexico"
    date = "12-12-2020"
    Nombre = "Pepe"
    Nombre2 = "Juana"
    curp_conyuge1 = "342435"
    curp_conyuge2 = "234525"
    domicilio2 = "Av Paseos"
    filename = "asd.jpg"
    filename2 = "asd.jpg"
    filename3 = "asd.jpg"
    evento = "Bodas"
    correo = "luizl067@gmail.com"
    return render_template("crea_tu_contrato_preview.html",location=location,date=date,Nombre=Nombre,Nombre2=Nombre2,curp_conyuge1=curp_conyuge1,curp_conyuge2=curp_conyuge2,domicilio2=domicilio2,filename=filename,filename2=filename2,filename3=filename3,correo=correo,evento=evento)

#VALIDAR CORREO

@app.route('/confirm', methods=['GET','POST'])
def confirm():
    if request.method == "POST":
        datos = request.get_json()
        print(datos)
        correo= datos['Correo']
        select=modelo.SelectId(correo)
        if select:
            resJSON={"alerta":"Si", "id": select[0]}
        else:
            resJSON={"alerta":"No"}
        return jsonify(resJSON)

#INSERTAR CONTRATO EN BD

@app.route('/confirmacion', methods=["POST","GET"])
def confirmacion():
    if request.method == "POST":
        datos = request.get_json()
        print(datos)
        location = datos['location']
        select_id_location = modelo.SelectBuscarIDSalon(location)
        id_location = select_id_location[0]
        print(id_location)
        date = datos['date']
        Nombre = datos['Nombre']
        Nombre2 = datos['Nombre2']
        curp_conyuge1 = datos['curp_conyuge1']
        curp_conyuge2 = datos['curp_conyuge2']
        domicilio2 = datos['domicilio2']
        filename = datos['filename']
        filename2 = datos['filename2']
        filename3 = datos['filename3']
        correo = datos['correo']
        evento = datos['evento']
        select_id_evento = modelo.SelectTipo(correo)
        print(select_id_evento)
        cliente = select_id_evento[0]
        id_evento = select_id_evento[1]
        print(location,date,Nombre,Nombre2,curp_conyuge1,curp_conyuge2,domicilio2,filename,filename2,filename3,correo,evento,cliente)
        #Imprimir BD
        print(Nombre,Nombre2,curp_conyuge1,curp_conyuge2,domicilio2,date,id_location,filename,filename2,filename3,id_evento,cliente)
        subir_contrato_BD =  modelo.InsertContratoBoda(Nombre,Nombre2,curp_conyuge1,curp_conyuge2,domicilio2,date,id_location,filename,filename2,filename3,id_evento,cliente)     
        if subir_contrato_BD:
            print("SI se inserto yeah")
        resJSON = {"alerta":"Si"}
        #modelo.InsertContrato(location,date,Nombre,Nombre2,curp_conyuge1,curp_conyuge2,domicilio2,filename,filename2,filename3)
        #tu_contrato = pdf_template_bodas_crea_tu_contrato(location,date,Nombre,Nombre2,curp_conyuge1,curp_conyuge2,domicilio2,filename,filename2,filename3)
        #print(tu_contrato)
        return jsonify(resJSON)

#Render PDF BODAS
@app.route('/pdf_template_bodas_crea_tu_contrato') #crea tu contrato bodas
def pdf_template_bodas_crea_tu_contrato(location,date,nombre_ine,nombre_ine2,curp_ine,curp2_ine,domicilio_ine,foto_ine,foto_ine2,foto_domicilio):
    #Modelo.entities(current_user.nombre,submit,"submit","current_date")
    print(foto_ine)
    rendered = render_template('pdf_template-crea-tu-contrato.html',date=date,location=location,nombre_ine=nombre_ine,nombre_ine2=nombre_ine2,curp_ine=curp_ine,curp2_ine=curp2_ine,domicilio_ine=domicilio_ine,foto_ine=foto_ine,foto_ine2=foto_ine2,foto_domicilio=foto_domicilio)
    #pdf = pdfkit.from_string(rendered,False,configuration = config)
    #Config para heroku    
    pdf = pdfkit.from_string(rendered,False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=bodas({nombre_ine},{nombre_ine2}).pdf'   
    return response

#Servicio Cognitivo --- Contratos --- Form para correo
@app.route('/crea_tu_contrato', methods=['GET','POST'])
def crea_tu_contrato():
    lugar_salon = modelo.SelectLugar()    
    form = MyForm()
    location = "None"
    date="None"
    correo = "None"
    error_ine = "El Archivo Seleccionado NO es una INE :("
    error_correo = "CORREO NO VALIDO"
    bandera_error = False
    if form.validate_on_submit():
        location = request.form["lc"]
        date = request.form["date"]
        correo = request.form["email"]
        ValidarCorreo = modelo.SelectId(correo)
        if ValidarCorreo:
            print(form.image.data)
            #print(form.image2.data)
            print(form.image3.data)
            filename = images.save(form.image.data)
            #filename2 = images.save(form.image2.data)
            filename3 = images.save(form.image3.data)
            print(f'./static/upload/img/{filename}')
            #print(f'./static/upload/img/{filename2}')
            print(f'./static/upload/img/{filename3}')
            print(location)
            print(date)
            ##INE 1
            image = open(f'./static/upload/img/{filename}','rb')
            #image = 'https://i.ibb.co/0rW9ZBv/20201122-182930.jpg'
            #recognize_handw_results = computervision_client.read(_url,language="es", raw=True)
            try:    
                recognize_handw_results = computervision_client.batch_read_file_in_stream(image,raw = True)
            except:
                print("No es una ine")
                return render_template('crea_tu_contrato_bodas.html',form=form,Error = error,error=error,lugar_salon=lugar_salon)
            image.close()
            operation_location_remote = recognize_handw_results.headers["Operation-Location"]
            operation_id = operation_location_remote.split("/")[-1]
            while True:            
                get_handw_text_results = computervision_client.get_read_operation_result(operation_id)
                if get_handw_text_results.status not in ['NotStarted', 'Running']:
                    break
                time.sleep(1)
                contador= ' '
            if get_handw_text_results.status == TextOperationStatusCodes.succeeded:
                for var in get_handw_text_results.recognition_results:
                    for linea in var.lines:
                        #print(linea.text)
                        contador=contador+ '\n' +linea.text
                        #print(" ") 
            
            print(contador)
            #hasta aqui me leyo la ine bien
            #import re
            bandera=""
            bandera = (r"INSTITUTO NACIONAL ELECTORAL\n"
            r"([a-zA-Z0-9]+.+)")
            bandera = re.findall(bandera, contador, re.MULTILINE)
            if len(bandera) >0:
                print("Si es una INE")
                if len(bandera) >0:
                    regex = (r"FECHA DE NACIMIENTO\n"
                    r"(\w+)\n"
                    r"(\d{2}/\d{2}/\d{4})\n"
                    r"(\w+)\n"
                    r"SEXO H\n"
                    r"([a-zA-Z0-9]+.+)\n")

                    domicilio = (r"DOMICILIO\n"
                    r"([a-zA-Z0-9]+.+)\n"
                    r"([a-zA-Z0-9]+.+)\n"
                    r"([a-zA-Z0-9]+.+)\n")

                    curp = (r"CURP ([a-zA-Z0-9]+.+)\n")

                    ApellidoPat = (r"FECHA DE NACIMIENTO\n"
                    r"(\w+)")

                    ApellidoPat = re.findall(ApellidoPat, contador, re.MULTILINE)
                    curp = re.findall(curp, contador, re.MULTILINE)
                    matches = re.findall(regex, contador, re.MULTILINE)
                    domicilio = re.findall(domicilio, contador, re.MULTILINE)
                    
                    

                    print(domicilio)
                    print(ApellidoPat)
                    print(matches)
                    print(curp)

                    try:
                        fecha=matches[0][1]
                        fecha2=fecha[6:10]+"-"+fecha[3:5]+"-"+fecha[0:2]
                    except:
                        fecha = "Hubo un error al Leer, Por Favor, Escribalo Manualmente"
                        fecha2 = "Hubo un error al Leer, Por Favor, Escribalo Manualmente" 
                    try:                   
                        domicilio2=domicilio[0][0]
                        domicilio2=domicilio2+ " " +domicilio[0][1]
                    except:
                        domicilio2 = "Hubo un error al Leer, Por Favor, Escribalo Manualmente"
                    try:
                        curp_conyuge1=curp[0]
                    except:
                        curp_conyuge1 = "Hubo un error al Leer, Por Favor, Escribalo Manualmente"
                    try:
                        Nombre=matches[0][0]+" "+matches[0][2]+" "+matches[0][3]
                    except:
                        Nombre = "Hubo un error al Leer, Por Favor, Escribalo Manualmente"

                    print("este es tu nombre: "+ Nombre)
                    print("este es tu curp: "+ curp_conyuge1)
                    print("este es tu domicilio: " + domicilio2)            
                    return crea_tu_contrato_preview_general(location,date,Nombre,curp_conyuge1,domicilio2,filename,filename3,correo)
                else:
                    return render_template('crea_tu_contrato.html',form=form,bandera=True,error=error_ine,lugar_salon=lugar_salon)
            else:
                return render_template('crea_tu_contrato.html',form=form,bandera=True,error=error_ine,lugar_salon=lugar_salon)
        else:
            return render_template('crea_tu_contrato.html',form=form,bandera=True,error=error_correo,lugar_salon=lugar_salon)
    return render_template('crea_tu_contrato.html',form=form,lugar_salon=lugar_salon)

@app.route('/crea_tu_contrato_preview_general', methods=["POST","GET"])
def crea_tu_contrato_preview_general(location,date,Nombre,curp_conyuge1,domicilio2,filename,filename3,correo):
    correo = correo
    ValidarCorreo = modelo.SelectId(correo)
    evento = ValidarCorreo[1]
    return render_template('crea_tu_contrato_preview_general.html', location=location,date=date,Nombre=Nombre,curp_conyuge1=curp_conyuge1,domicilio2=domicilio2,filename=filename,filename3=filename3,correo=correo,evento=evento)

#DEBUG FORM GENERAL
@app.route('/confirmacion_de_contrato', methods=["POST","GET"])
def confirmacion_de_contrato():
    location= "Mexico"
    date = "12-12-2020"
    Nombre = "Pepe"
    Nombre2 = "Juana"
    curp_conyuge1 = "342435"
    curp_conyuge2 = "234525"
    domicilio2 = "Av Paseos"
    filename = "asd.jpg"
    filename2 = "asd.jpg"
    filename3 = "asd.jpg"
    correo = "luiz@gmail.com"
    ValidarCorreo = modelo.SelectId(correo)
    evento = ValidarCorreo[1]
    print(ValidarCorreo)
    print(evento)
    return render_template("crea_tu_contrato_preview_general.html",location=location,date=date,Nombre=Nombre,Nombre2=Nombre2,curp_conyuge1=curp_conyuge1,curp_conyuge2=curp_conyuge2,domicilio2=domicilio2,filename=filename,filename2=filename2,filename3=filename3,correo=correo,evento=evento)

#INSERTAR CONTRATO GENERAL EN BD
@app.route('/confirmacion_general', methods=["POST","GET"])
def confirmacion_general():
    if request.method == "POST":
        datos = request.get_json()
        print(datos)
        location = datos['location']
        select_id_location = modelo.SelectBuscarIDSalon(location)
        id_location = select_id_location[0]
        print(id_location)
        date = datos['date']
        Nombre = datos['Nombre']
        #Nombre2 = datos['Nombre2']
        curp_conyuge1 = datos['curp_conyuge1']
        #curp_conyuge2 = datos['curp_conyuge2']
        domicilio2 = datos['domicilio2']
        filename = datos['filename']
        #filename2 = datos['filename2']
        filename3 = datos['filename3']
        correo = datos['correo']
        evento = datos['evento']
        select_id_evento = modelo.SelectTipo(correo)
        print(select_id_evento)
        cliente = select_id_evento[0]
        id_evento = select_id_evento[1]
        print(location,date,Nombre,curp_conyuge1,domicilio2,filename,filename3,correo,evento,cliente)
        #Imprimir BD
        print(Nombre,curp_conyuge1,domicilio2,date,id_location,filename,filename3,id_evento,cliente)
        subir_contrato_GN = modelo.InsertContratoGeneral(Nombre,curp_conyuge1,domicilio2,date,id_location,filename,filename3,id_evento,cliente)
        #subir_contrato_BD =  modelo.InsertContratoBoda(Nombre,Nombre2,curp_conyuge1,curp_conyuge2,domicilio2,date,id_location,filename,filename2,filename3,id_evento,cliente)     
        if subir_contrato_GN:
            return print("SI se inserto yeah")       
        resJSON = {"alerta":"Si"}
        #modelo.InsertContrato(location,date,Nombre,Nombre2,curp_conyuge1,curp_conyuge2,domicilio2,filename,filename2,filename3)
        #tu_contrato = pdf_template_bodas_crea_tu_contrato(location,date,Nombre,Nombre2,curp_conyuge1,curp_conyuge2,domicilio2,filename,filename2,filename3)
        #print(tu_contrato)
        return jsonify(resJSON)

@app.route('/pdf_template_general_crea_tu_contrato') #crea tu contrato bodas
def pdf_template_general_crea_tu_contrato(location,date,nombre_ine,curp_ine,domicilio_ine,foto_ine,foto_domicilio,correo,evento):
    #Modelo.entities(current_user.nombre,submit,"submit","current_date")
    print(foto_ine)
    rendered = render_template('pdf_template-crea-tu-contrato_general.html',date=date,location=location,nombre_ine=nombre_ine,curp_ine=curp_ine,domicilio_ine=domicilio_ine,foto_ine=foto_ine,foto_domicilio=foto_domicilio)
    #pdf = pdfkit.from_string(rendered,False,configuration = config)
    #Config para heroku    
    pdf = pdfkit.from_string(rendered,False,configuration = config)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=evento_de_({nombre_ine}).pdf'   
    return response
@app.route('/<location>/<date>/<nombre_ine>/<curp_ine>/<domicilio_ine>/<foto_ine>/<foto_domicilio>/<evento>/<correo>') #crea tu contrato bodas
def pdf_template_general_crea_tu_contrato_get(location,date,nombre_ine,curp_ine,domicilio_ine,foto_ine,foto_domicilio,correo,evento):
    #Modelo.entities(current_user.nombre,submit,"submit","current_date")
    print(foto_ine)
    rendered = render_template('pdf_template-crea-tu-contrato_general.html',date=date,location=location,Nombre=nombre_ine,curp_conyuge1=curp_ine,domicilio2=domicilio_ine,foto_ine=foto_ine,foto_domicilio=foto_domicilio,correo=correo,evento=evento)
    #pdf = pdfkit.from_string(rendered,False,configuration = config)
    #Config para heroku    
    pdf = pdfkit.from_string(rendered,False,configuration = config)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=evento_de_({nombre_ine}).pdf'   
    return response

@app.route('/<location>/<date>/<nombre_ine>/<nombre_ine2>/<curp_ine>/<curp2_ine>/<domicilio_ine>/<foto_ine>/<foto_ine2>/<foto_domicilio>/<correo>/<evento>') #crea tu contrato bodas
def pdf_template_bodas_crea_tu_contrato_get(location,date,nombre_ine,nombre_ine2,curp_ine,curp2_ine,domicilio_ine,foto_ine,foto_ine2,foto_domicilio,correo,evento):
    #Modelo.entities(current_user.nombre,submit,"submit","current_date")
    print(foto_ine)
    rendered = render_template('pdf_template-crea-tu-contrato.html',date=date,location=location,nombre_ine=nombre_ine,nombre_ine2=nombre_ine2,curp_ine=curp_ine,curp2_ine=curp2_ine,domicilio_ine=domicilio_ine,foto_ine=foto_ine,foto_ine2=foto_ine2,foto_domicilio=foto_domicilio,correo=correo,evento=evento)
    #pdf = pdfkit.from_string(rendered,False,configuration = config)
    #Config para heroku    
    pdf = pdfkit.from_string(rendered,False,configuration = config)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=bodas({nombre_ine},{nombre_ine2}).pdf'   
    return response

