import json
from flask import Flask, jsonify, request,render_template, redirect, url_for, flash, Blueprint
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
business_blueprint = Blueprint('business_blueprint', __name__)

conexion = MySQL(app)
CORS(app)

# INICIO APARTADO EMPRESAS

@business_blueprint.route('/business')
def IndexBusiness():
    return '<h1> BUSINESS </h1>'

@business_blueprint.route('/business/list', methods=['GET'])
def ListBusiness():
    try:
        cursor = conexion.connection.cursor()
        getActiveBusiness = "SELECT * FROM empresa WHERE Desactivado = 0"
        cursor.execute(getActiveBusiness)
        businessList = cursor.fetchall()
        businessArr=[]

        for fila in businessList:
            business={'IdEmpresa':fila[0],'Nombre':fila[1], "Desactivado":fila[2]}
            businessArr.append(business)
            print(business)
        return jsonify(businessArr)
    except Exception:
        return jsonify({'Message':"Error at Business List Method"})

@business_blueprint.route('/business/<IdEmpresa>', methods={'GET'})
def getBusinessById(IdEmpresa):
    try:
        cursor = conexion.connection.cursor()
        businessFound = "SELECT * FROM empresa WHERE IdEmpresa = '{0}'".format(IdEmpresa)
        cursor.execute(businessFound)
        businessData = cursor.fetchone()

        if businessData != None:
            business={'IdEmpresa':businessData[0],'Nombre':businessData[1], "Desactivado":businessData[2]}
            return jsonify({'Business': business, 'Message':"Business Found!"})
        else:
            return jsonify({'Message':"Business not Found!"})
    except Exception as ex:
        return jsonify({'Message':"{0}".format(ex)})

@business_blueprint.route('/business', methods=['POST'])
def AddBusiness():
    try:
        print(request.json)
        if request.method == 'POST':
            cursor = conexion.connection.cursor()
            insertBusiness = "INSERT INTO empresa (Nombre) VALUES ('{0}')".format(request.json['businessName'])
            print("insertBusiness --> " , insertBusiness)
            cursor.execute(insertBusiness)
            conexion.connection.commit()
            return jsonify({'mensaje':"Business Added!"})
    except Exception as ex:
        return jsonify({'mensaje':"The business already exists"})

@business_blueprint.route('/business/<IdEmpresa>', methods=['DELETE'])
def DeleteBusiness(IdEmpresa):
    try:
        cursor = conexion.connection.cursor()

        existBusiness = "SELECT * FROM empresa WHERE IdEmpresa = '{}'".format(IdEmpresa)
        cursor.execute(existBusiness)

        isEnableResult = cursor.fetchone()
        print(isEnableResult)

        if isEnableResult[0] != None:
            deleteBusiness = "UPDATE empresa SET Desactivado = 1 WHERE IdEmpresa = {0}".format(IdEmpresa)
            print(deleteBusiness)
            cursor.execute(deleteBusiness)
            conexion.connection.commit()
            return jsonify({'message':"Business Deleted!"})
        else:
            return jsonify({'message':"Business not found!!"})
    except Exception as ex:
        return jsonify({'message':"Error in Business Delete Method!"})

@business_blueprint.route('/business/<IdEmpresa>', methods=['PUT'])
def UpdateBusiness(IdEmpresa):    
    
    try:
        cursor = conexion.connection.cursor()
        findBusiness = "SELECT * FROM empresa WHERE IdEmpresa = {0}".format(IdEmpresa)

        cursor.execute(findBusiness)
        businessFound = cursor.fetchone()

        if businessFound != None:
            updateBusiness = "UPDATE empresa SET Nombre = '{0}' WHERE IdEmpresa = {1}".format(request.json["businessName"], IdEmpresa)
            print(updateBusiness)
            cursor.execute(updateBusiness)
            conexion.connection.commit()
            return jsonify({'Message':"Updated Business"})
        else:
            return jsonify({'Message':"Business not Found!"})
    except Exception as ex:
        return jsonify({'Message':ex})



# FIN APARTADO EMPRESAS