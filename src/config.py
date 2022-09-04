class DevelopmentConfig():
    #MySql Connetion
    DEBUG=True
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ""
    MYSQL_DB = "superratas"
    

config = {
    'development': DevelopmentConfig
}