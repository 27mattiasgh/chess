import socket
import netaddr

class Multiplayer:
    def __init__(self):
        self.opponent_ip = None
        self.setup = True


    #ACTUAL
    def send(self, msg):
        server = (str(self.opponent_ip), 4000)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((str(socket.gethostbyname(socket.gethostname())), 4000))
        print('user actual: attempting to transfer data')
        
        while True:
            data = bytes(msg, encoding='utf-8')
            s.sendto(data, server)
            print('user actual: data transfer complete')
            return

    def recv(self):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((str(socket.gethostbyname(socket.gethostname())), 4000))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print('host actual: waiting for connection')

            while True:
                data, addr = s.recvfrom(1024)
                print('host actual: connection established, data received: ', data)
                return str(data)

    

    #SETUP
    def client_setup(self, msg):
        server = (str(self.opponent_ip), 4000)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((str(socket.gethostbyname(socket.gethostname())), 4000))
        print('user setup: attempting to transfer data')
        
        while True:
            data = bytes(msg, encoding='utf-8')
            s.sendto(data, server)
            print('user setup: data transfer complete')
            return
        
        
        
    def host_setup(self):
            print(s.getsockname()[0], 'ip')

            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((str(socket.gethostbyname(socket.gethostname())), 4000))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print('host actual: waiting for connection')

            while True:
                data, addr = s.recvfrom(1024)
                print('host actual: connection established, data received: ', data, 'addr: ', addr) 
                
                self.set_opponent_ip(addr) #SET address to addr recived

                return str(data)



    def set_opponent_ip(self, code):
        self.opponent_ip = str(netaddr.IPAddress(code))