from flask import Flask, jsonify, request,render_template, redirect, url_for, flash, Blueprint
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
points_blueprint = Blueprint('points_blueprint', __name__)
 
conexion = MySQL(app)

# INICIO APARTADO TIPO_PUNTO

@points_blueprint.route('/points')
def IndexPoint():
    return '<h1> POINTS </h1>'

@points_blueprint.route('/points/list')
def ListPoints():
    try:
        cursor = conexion.connection.cursor()
        getActivePoints = "SELECT * FROM tipopunto WHERE desactivado = 0"
        cursor.execute(getActivePoints)
        pointsList = cursor.fetchall()
        pointsArr=[]
        
        for fila in pointsList:
            pointType = {
                'IdPunto':fila[0],
                'IdEmpresa':fila[1], 
                'NombrePunto':fila[2],
                'Descripcion':fila[3],
                'Desactivado':fila[4]               
            }
            pointsArr.append(pointType)
        
        return jsonify(pointsArr)
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

@points_blueprint.route('/points/<IdPunto>', methods={'GET'})
def GetPointById(IdPunto):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM tipopunto WHERE IdPunto = '{0}'".format(IdPunto)
        cursor.execute(sql)
        datos = cursor.fetchone()  
                
        if datos != None:
            tipo_punto = {
                'IdPunto':datos[0],
                'IdEmpresa':datos[1], 
                'NombrePunto':datos[2],
                'Descripcion':datos[3],
                'Desactivado':datos[4]               
            }
            return jsonify({'Tipo Punto': tipo_punto, 'mensaje':"Tipo de Punto Encontrado!"})
        else:
            return jsonify({'mensaje':"Tipo de Punto no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

@points_blueprint.route('/points', methods=['POST'])
def AddPoint():
    try:
        cursor = conexion.connection.cursor()
                
        insertarPunto = """INSERT INTO tipopunto (IdEmpresa, NombrePunto, Descripcion) 
                VALUES ({0}, '{1}', '{2}')""".format(request.json["IdEmpresa"], request.json["NombrePunto"], request.json["Descripcion"])            
        cursor.execute(insertarPunto)
        conexion.connection.commit()
        return jsonify({'mensaje':"Tipo de Punto Guardado!"})
    except Exception as ex:
        return jsonify({'mensaje':"Error!"})

@points_blueprint.route('/points/<IdPunto>', methods={'DELETE'})
def DeletePoint(IdPunto):
    try:        
        cursor = conexion.connection.cursor()
        
        isEnable = "SELECT Desactivado FROM tipopunto WHERE IdPunto = '{0}'".format(IdPunto)
        cursor.execute(isEnable)
        
        isEnableResult = cursor.fetchone()
        
        if isEnableResult[0] == 0: # PUEDE DESACTIVARSE POR QUE ESTA ACTIVO 
            cursor = conexion.connection.cursor()      
            desactivarPunto = "UPDATE tipopunto SET Desactivado = !Desactivado WHERE IdPunto = {0}".format(IdPunto)        
            cursor.execute(desactivarPunto)
        
            conexion.connection.commit()
            return jsonify({'mensaje':"Tipo Punto Eliminado!"}) 
        else:
            cursor = conexion.connection.cursor()      
            desactivarPunto = "UPDATE tipopunto SET Desactivado = !Desactivado WHERE IdPunto = {0}".format(IdPunto)        
            cursor.execute(desactivarPunto)
        
            conexion.connection.commit()
            return jsonify({'mensaje':"Tipo Punto Reactivado!"})
    except Exception as ex:
        return jsonify({'mensaje':"Error!"})
    
# FIN APARTADO TIPO_PUNTO