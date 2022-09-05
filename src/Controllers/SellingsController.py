from ctypes.wintypes import PINT
from time import time
from flask import Flask, jsonify, request, Blueprint
from flask_mysqldb import MySQL
import datetime

app = Flask(__name__)
sellings_blueprint = Blueprint('sellings_blueprint', __name__)
 
conexion = MySQL(app)

@sellings_blueprint.route('/sellings')
def SellingsIndex():
    return '<h1> SELLINGS </h1>'

@sellings_blueprint.route('/sellings/list', methods=['GET'])
def ListSellings():
    try:
        cursor = conexion.connection.cursor()
        getAllSellings = "SELECT * FROM ventas"
        cursor.execute(getAllSellings)
        sellingsList = cursor.fetchall()
        sellingsArr=[]
        
        for fila in sellingsList:
            selling={
                'IdVenta':fila[0],
                'IdPublicacion':fila[1], 
                'rutCliente':fila[2],
                'tipoPunto':fila[3],
                'puntosConvertidos':fila[4],
                'tasaConversion':fila[5],
                'valorCLP':fila[6],
                'fechaOperacion':fila[7]
            }
                
            sellingsArr.append(selling)
            print(selling)        
        return jsonify(sellingsArr)
    except Exception:
        return jsonify({'Message':"Error at Selling List Method"})

@sellings_blueprint.route('/sellings/add/<IdPublicacion>', methods=['POST'])
def AddSelling(IdPublicacion):
    try:
        
        if request.method == 'POST':            
            cursor = conexion.connection.cursor()
            
            pointsToConvert = request.json['ClientPoints']
            
            # 1. Primero buscamos al cliente y recuperamos sus puntos minimos
            searchUser = "SELECT * FROM usuario WHERE ClienteRut = '{0}'".format(request.json['ClientRut'])
            
            cursor.execute(searchUser)
            userFound = cursor.fetchone() 
            
            if userFound != None:   
                            
                userTotalPoints = int(userFound[5])
                print("HASTA AQUI TODA LA INFO DE ATRAS VIENE CORRECTA")
                print("userTotalPoints --> ", userTotalPoints)
                
                # 2. verificamos que los puntos enviados en el post no excedan el total de puntos del cliente
                print("pointsToConvert > 0 --> ", pointsToConvert > 0)
                if (pointsToConvert > 0): 
                    
                    print("pointsToConvert <= userTotalPoints --> ", pointsToConvert <= userTotalPoints)
                    if (pointsToConvert <= userTotalPoints):
                        # 3. verificamos que los puntos enviados en el post cumplan con los puntos minimos de conversion de la publicacion
                        searchPublication = "SELECT * FROM publicacion WHERE IdPublicacion = '{0}'".format(IdPublicacion)
                        print("QUERY SEARCH PUBLICATION --> ", searchPublication)
                        
                        cursor.execute(searchPublication)
                        publicationFound = cursor.fetchone()
                    
                        if publicationFound != None:
                            publicationMinimusPoints = publicationFound[5]
                            convertionRate = publicationFound[6]                   
                                        
                            if pointsToConvert > publicationMinimusPoints:
                                
                                # 4. calculamos la diferencia de puntos que le queda al cliente y la conversion a CLP
                                remainingPoints = userTotalPoints - pointsToConvert                            
                                pointsToCLP = pointsToConvert * convertionRate
                                
                                # 5. Actualizamos la info del cliente con los nuevos puntos
                                updateClientData = "UPDATE usuario SET TotalPuntos = {0} WHERE ClienteRut = '{1}'".format(remainingPoints, request.json['ClientRut'])
                                cursor.execute(updateClientData)
                                conexion.connection.commit()  
                                
                                # 6. obtenemos la fecha de la operacion
                                operationDate = datetime.datetime.now()
                                formatedDate = operationDate.strftime("%y-%m-%d %H:%M:%S")
                                
                                print("Llegando al insert de la venta")
                                
                                # 7. finalmente insertamos en la tabla de registro de ventas
                                insertSell = """INSERT INTO ventas(IdPublicacion, rutCliente, tipoPunto, puntosConvertidos, tasaConversion, valorCLP, fechaOperacion) 
                                    VALUES ({0},'{1}', {2}, {3}, {4}, {5}, '{6}')""".format(IdPublicacion, request.json['ClientRut'],
                                        request.json['TypePoint'], pointsToConvert, convertionRate, pointsToCLP, formatedDate)
                                
                                print(insertSell)
                                
                                cursor.execute(insertSell)
                                conexion.connection.commit()  
                                
                                return jsonify({'Message':"Selling Added"})
                            else:
                                return jsonify({'Message':"No cumple con la cantidad minima de puntos para converir!"}) 
                        else:
                            return jsonify({'Message':"Publication not Found!"}) 
                    else:
                        return jsonify({'Message':"Los puntos ingresados excenden su total de puntos!"})                         
                else:
                    return jsonify({'Message':"Los puntos a convertir son 0!"})
            else:
                return jsonify({'Message':"User not found Found!"})
    except Exception as ex:
        return jsonify({'mensaje':"Error to Add Selling"})