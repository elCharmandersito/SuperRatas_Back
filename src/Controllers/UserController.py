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
        sql = "SELECT * FROM usuario WHERE Desactivado = 0"
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
        if request.method == 'POST':            
            cursor = conexion.connection.cursor()
            insertUser = """INSERT INTO usuario (ClienteRut, ClienteDV, Nombre, Apellido, TotalPuntos) 
                VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(request.json['userRut'], request.json['userDv'], request.json['userName'], request.json['userLastName'],request.json['userPoints'])
            
            print(insertUser)
            cursor.execute(insertUser)
            conexion.connection.commit()
            return jsonify({'mensaje':"User Added!"})
    except Exception as ex:
        return jsonify({'mensaje':"The user already exists"})

@user_blueprint.route('/user/<ClienteRut>', methods=['DELETE'])
def DeleteBusiness(ClienteRut):
    try:
        cursor = conexion.connection.cursor()

        existClient = "SELECT * FROM usuario WHERE ClienteRut = '{}'".format(ClienteRut)
        cursor.execute(existClient)

        isEnableResult = cursor.fetchone()
        print(isEnableResult)

        if isEnableResult[0] != None:
            deleteUser = "UPDATE usuario SET Desactivado = 1 WHERE ClienteRut = {0}".format(ClienteRut)
            print(deleteUser)
            cursor.execute(deleteUser)
            conexion.connection.commit()
            return jsonify({'message':"User Deleted!"})
        else:
            return jsonify({'message':"User not found!!"})
    except Exception as ex:
        return jsonify({'message':"Error in User Delete Method!"})


# FIN APARTADO USUARIO