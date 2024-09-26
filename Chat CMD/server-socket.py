import socket
import threading
import sys
import os

class Servidor():
    def __init__(self, host="localhost", port=7000):
        self.clientes = []
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)
        
        # Hilos para aceptar y procesar conexiones
        aceptar = threading.Thread(target=self.aceptarCon)
        procesar = threading.Thread(target=self.procesarCon)
        aceptar.daemon = True 
        aceptar.start()
        procesar.daemon = True 
        procesar.start()

        try:
            while True:
                msg = input('-> ')
                if msg == 'salir':
                    break
            self.sock.close()
            sys.exit()
        except:
            self.sock.close()
            sys.exit()

    def procesarComando(self, comando, cliente):
        # Procesa el comando del cliente
        if comando == "lsFiles":
            # Listar archivos en la carpeta "Files"
            if os.path.exists("Files"):
                archivos = os.listdir("Files")
                archivos_str = "\n".join(archivos)
            else:
                archivos_str = "La carpeta 'Files' no existe."
            cliente.send(archivos_str.encode())
        elif comando.startswith("get"):
            # Enviar archivo solicitado
            archivo_nombre = comando.split(" ")[1]
            archivo_ruta = os.path.join("Files", archivo_nombre)
            if os.path.exists(archivo_ruta):
                with open(archivo_ruta, "rb") as archivo:
                    cliente.send(archivo.read())
            else:
                cliente.send(f"Archivo {archivo_nombre} no encontrado.".encode())
        else:
            cliente.send("Comando no reconocido.".encode())

    def aceptarCon(self):
        print("Aceptar conexiones iniciado")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clientes.append(conn)
            except:
                pass

    def procesarCon(self):
        print("Procesar conexiones iniciado")
        while True:
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c.recv(1024).decode()
                        if data:
                            print(f"Comando recibido: {data}")
                            # Procesar el comando recibido
                            self.procesarComando(data, c)
                    except:
                        pass

server = Servidor()
