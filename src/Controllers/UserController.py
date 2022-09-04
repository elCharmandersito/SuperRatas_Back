from flask import Flask, jsonify, request,render_template, redirect, url_for, flash, Blueprint
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
user_blueprint = Blueprint('user_blueprint', __name__) 
conexion = MySQL(app)

CORS(app)

# INICIO APARTADO USUARIO

@user_blueprint.route('/user')
def UserIndex():
    return '<h1> USERS </h1>'

@user_blueprint.route('/user/list')
def ListUsers():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM usuario"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios=[]
        
        ## HACEMOS LA CONSULTA A LA BASE DE DATOS PARA RECUPERAR LAS EMPRESAS QUE ESTAN DISPONIBLES
        for fila in datos:
            usuario = {
                'IdUsuario':fila[0],
                'ClienteRut':fila[1], 
                'ClienteDV':fila[2],
                'Nombre':fila[3],
                'Apellido':fila[4],
                'TotalPuntos':fila[5]                
            }
            usuarios.append(usuario)
        
        return jsonify(usuarios)
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

@user_blueprint.route('/user/<ClienteRut>', methods={'GET'})
def GetUserByRut(ClienteRut):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM usuario WHERE CLienteRut = '{0}'".format(ClienteRut)
        cursor.execute(sql)
        datos = cursor.fetchone()  
                
        if datos != None:
            usuario = {
                'IdUsuario':datos[0],
                'ClienteRut':datos[1], 
                'ClienteDV':datos[2],
                'Nombre':datos[3],
                'Apellido':datos[4],
                'TotalPuntos':datos[5]                
            }
            return jsonify({'usuario': usuario, 'mensaje':"Usuario Encontrado!"})
        else:
            return jsonify({'mensaje':"Usuario no encontrada"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

@user_blueprint.route('/user', methods=['POST'])
def AddUser():
    try:
        cursor = conexion.connection.cursor()
                
        rutUsuario = request.json["ClienteRut"]
           
        buscarUsuario = "SELECT COUNT(ClienteRut) FROM usuario WHERE ClienteRUt = {0}".format(rutUsuario)
        
        cursor.execute(buscarUsuario)
        datos = cursor.fetchone()
                
        if datos[0] == 0:            
            
            insertarUsuario = """INSERT INTO usuario (ClienteRut, ClienteDV, Nombre, Apellido, TotalPuntos) 
                VALUES ({0}, '{1}', '{2}', '{3}', {4})""".format(request.json["ClienteRut"], request.json["ClienteDV"], 
                                                                 request.json["Nombre"], request.json["Apellido"], 
                                                                 request.json["TotalPuntos"])            
            cursor.execute(insertarUsuario)
            conexion.connection.commit()
            return jsonify({'mensaje':"Usuario Guardada!"})
        else:
            return jsonify({'mensaje':"Usuario Duplicada!"})
    except Exception as ex:
        return jsonify({'mensaje':"Error!"})

# FIN APARTADO USUARIO