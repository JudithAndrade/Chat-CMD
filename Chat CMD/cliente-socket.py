import socket
import threading
import sys
import os

class Cliente():
    def __init__(self, host="localhost", port=7000):
        try:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.connect((str(host), int(port)))
            msg_recv = threading.Thread(target=self.msg_recv)
            msg_recv.daemon = True 
            msg_recv.start()

            while True:
                msg = input('-> ')
                if msg != 'salir':
                    self.send_msg(msg)
                else:
                    self.sock.close()
                    sys.exit()
        except:
            print("Error al conectar el socket")
            
    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(4096)
                if data:
                    # Verificar si es un archivo recibido
                    if b'\x00' in data:
                        archivo_nombre = data.split(b'\x00')[0].decode()
                        archivo_datos = data.split(b'\x00')[1]

                        if not os.path.exists("download"):
                            os.makedirs("download")

                        with open(os.path.join("download", archivo_nombre), "wb") as archivo:
                            archivo.write(archivo_datos)

                        print(f"Archivo {archivo_nombre} descargado en la carpeta 'download'.")
                    else:
                        print(data.decode())
            except:
                pass

    def send_msg(self, msg):
        try:
            self.sock.send(msg.encode())
        except:
            print('Error al enviar el mensaje')

cliente = Cliente()
