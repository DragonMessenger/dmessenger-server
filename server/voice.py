#!/usr/bin/python3

# Library for colors
from colorama import init, Fore
from colorama import Back
from colorama import Style

# Init methods
init(autoreset=True)

recieveBytes = 2048

# Logo
print('██████╗ ███╗   ███╗███████╗███████╗███████╗███████╗███╗   ██╗ ██████╗ ███████╗██████╗')
print('██╔══██╗████╗ ████║██╔════╝██╔════╝██╔════╝██╔════╝████╗  ██║██╔════╝ ██╔════╝██╔══██╗')
print('██║  ██║██╔████╔██║█████╗  ███████╗███████╗█████╗  ██╔██╗ ██║██║  ███╗█████╗  ██████╔╝')
print('██║  ██║██║╚██╔╝██║██╔══╝  ╚════██║╚════██║██╔══╝  ██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗')
print('██████╔╝██║ ╚═╝ ██║███████╗███████║███████║███████╗██║ ╚████║╚██████╔╝███████╗██║  ██║')
print('╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝')
print()
print(Fore.YELLOW + '           Voice | Server | Alpha 22.03.2022 | DragonFire Community')

import socket
import threading

class Server:
    def __init__(self):
            self.ip = socket.gethostbyname(socket.gethostname())
            while 1:
                try:
                    self.port = 7002

                    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.s.bind((self.ip, self.port))

                    break
                except:
                    print(Fore.RED + "[Error] Couldn't bind to that port")

            self.connections = []
            self.accept_connections()

    def accept_connections(self):
        self.s.listen(100)

        print(Fore.CYAN + '[Info] Running on IP: '+self.ip)
        print(Fore.CYAN + '[Info] Running on port: '+str(self.port))
        
        while True:
            c, addr = self.s.accept()

            print(Back.GREEN + f'[Voice] Connected: {addr}')

            self.connections.append(c)

            threading.Thread(target=self.handle_client,args=(c,addr,)).start()
        
    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data)
                except:
                    pass

    def handle_client(self,c,addr):
        while 1:
            try:
                data = c.recv(recieveBytes)
                self.broadcast(c, data)
            
            except socket.error:
                c.close()

server = Server()