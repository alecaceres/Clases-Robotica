import socketio


class Client():
    sio=socketio.Client()
    clients={}
    server="http://localhost:5555"
    user=""
    def __init__(self,server,user=user):
        self.server=server
        self.user=user
        self.sio.connect(self.server)
        self.sio.on("client",self.fromServer)


    def fromServer(self,json):
        self.clients={**json}

    def getClients(self):
        return self.clients

    def update(self,data,user=None):
        user_=self.user if not user else user
        self.sio.emit('update', {'label':user_,'data':data})



#Clase utilizada para conexion con el server
#   params
#       - server: URL del servidor a conectar
#   out 
#       - out: La funcion getClients devuelve las posiciones de todos los demas conectados



# EXAMPLE
# import time
# server="http://5bff5eecaae6.ngrok.io"
# cl=Client(server)


# while(1):
#     time.sleep(2)
#     cl.update({'foo':'bar'},"soy un qr text")
#     print("clients", cl.clients)
    




