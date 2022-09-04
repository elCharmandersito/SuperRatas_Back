from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS

from config import config

# controllers import
from Controllers.BusinessController import business_blueprint
from Controllers.UserController import user_blueprint
from Controllers.PublicationController import publication_blueprint
from Controllers.PointsController import points_blueprint
from Controllers.SellingsController import sellings_blueprint

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# REGISTER TO THE CONTROLLER
app.register_blueprint(business_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(publication_blueprint)
app.register_blueprint(points_blueprint)
app.register_blueprint(sellings_blueprint)
 
conexion = MySQL(app)
CORS(app)

# DEFAULT INDEX

@app.route('/')
def app_home():
    return '<h1> Bienvenidos a Super Ratas App </h1>'

def pagina_no_encontrada(error):
    return "<h1> LA PAGINA QUE BUSCAS NO SE ENCUENTRA .... </h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.secret_key = 'super_ratas_key'
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()