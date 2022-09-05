from hashlib import new
from flask import Flask, jsonify, request,render_template, redirect, url_for, flash, Blueprint
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
publication_blueprint = Blueprint('publication_blueprint', __name__)
 
conexion = MySQL(app)

# INICIO APARTADO PUBLICACION

@publication_blueprint.route('/publication')
def PublicationIndex():
    return '<h1> PUBLICATION </h1>'

@publication_blueprint.route('/publication/list')
def ListPublications():
    try:
        cursor = conexion.connection.cursor()
        getAllActivePublication = "SELECT * FROM publicacion WHERE Desactivado = 0"
        cursor.execute(getAllActivePublication)
        publicationsList = cursor.fetchall()
        publicationsArr=[]
        
        for fila in publicationsList:
            publication = {
                'IdPublicacion':fila[0],
                'IdPunto':fila[1], 
                'IdUsuario':fila[2],
                'NombrePublicacion':fila[3],
                'Descripcion':fila[4],
                'PuntosMinimos':fila[5],
                'TasaCambio':fila[6],
                'Estado':fila[7],
                'Desactivado':fila[8]                  
            }
            publicationsArr.append(publication)
        
        return jsonify(publicationsArr)
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

@publication_blueprint.route('/publication/<IdPublicacion>', methods={'GET'})
def GetPublicationById(IdPublicacion):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM publicacion WHERE IdPublicacion = '{0}'".format(IdPublicacion)
        cursor.execute(sql)
        datos = cursor.fetchone()  
                
        if datos != None:
            publicacion = {
                'IdPublicacion':datos[0],
                'IdPunto':datos[1], 
                'IdUsuario':datos[2],
                'NombrePublicacion':datos[3],
                'Descripcion':datos[4],
                'PuntosMinimos':datos[5],
                'TasaCambio':datos[6],
                'Esatado':datos[7],
                'Desactivado':datos[8]                  
            }
            return jsonify({'publicacion': publicacion, 'mensaje':"Publicacion Encontrado!"})
        else:
            return jsonify({'mensaje':"Publicacion no encontrada"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

@publication_blueprint.route('/publication', methods=['POST'])
def AddPublication():
    try:        
        cursor = conexion.connection.cursor()
                        
        pubName = request.json["PubName"]   
                
        searchPublication = "SELECT COUNT(NombrePublicacion) FROM publicacion WHERE NombrePublicacion = '{0}'".format(pubName)
                
        cursor.execute(searchPublication)
        datos = cursor.fetchone()
                
        if datos[0] == 0:            
            
            insertarPublicacion = """INSERT INTO publicacion (IdPunto, IdUsuario, NombrePublicacion, Descripcion, PuntosMinimos, TasaCambio) 
                VALUES ({0}, {1}, '{2}', '{3}', {4}, {5})""".format(request.json["IdPoint"], request.json["IdUser"], 
                                                                 request.json["PubName"], request.json["Description"], 
                                                                 request.json["MinimosPoint"], request.json["ConvertedRate"]) 
            cursor.execute(insertarPublicacion)
            conexion.connection.commit()
            return jsonify({'mensaje':"Publicacion Guardada!"})
        else:
            return jsonify({'mensaje':"Publicacion Duplicada!"})
    except Exception as ex:
        return jsonify({'mensaje':"Error!"})

@publication_blueprint.route('/publication/<IdPublicacion>', methods={'DELETE'})
def DeletePublication(IdPublicacion):
    try:        
        cursor = conexion.connection.cursor()
        
        isEnable = "SELECT Desactivado FROM publicacion WHERE IdPublicacion = '{}'".format(IdPublicacion)
        cursor.execute(isEnable)
        
        isEnableResult = cursor.fetchone()
        
        if isEnableResult[0] == 0: # PUEDE DESACTIVARSE POR QUE ESTA ACTIVO 
            cursor = conexion.connection.cursor()      
            desactivarPublicacion = "UPDATE publicacion SET Desactivado = !Desactivado WHERE IdPublicacion = {0}".format(IdPublicacion)        
            cursor.execute(desactivarPublicacion)
        
            conexion.connection.commit()
            return jsonify({'mensaje':"Publicacion Eliminada!"}) 
        else:
            cursor = conexion.connection.cursor()      
            desactivarPublicacion = "UPDATE publicacion SET Desactivado = !Desactivado WHERE IdPublicacion = {0}".format(IdPublicacion)        
            cursor.execute(desactivarPublicacion)
        
            conexion.connection.commit()
            return jsonify({'mensaje':"Publicacion Reactivada!"}) 
    except Exception as ex:
        return jsonify({'mensaje':"Error!"})

@publication_blueprint.route('/publication/<IdPublicacion>', methods={'PUT'})
def UpdatePublicationStatus(IdPublicacion):
    try:        
        cursor = conexion.connection.cursor()
        
        newState = ""
        
        if request.json["Estado"].lower() == "borrador":
            newState = "borrador"
        elif request.json["Estado"].lower() == "publicado":
            newState = "publicado"
        elif request.json["Estado"].lower() == "vendido":
            newState = "vendido"
        
        updatePublication = "UPDATE publicacion SET Estado = '{0}' WHERE IdPublicacion = {1}".format(newState, IdPublicacion)  
            
        cursor.execute(updatePublication)        
        conexion.connection.commit()
        return jsonify({'Message':'Publication Updated!'}) 
    except Exception as ex:
        return jsonify({'Message':'Update Failed!'}) 

# FIN APARTADO PUBLICACION