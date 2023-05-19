import socket
import netaddr


class Multiplayer:
    def __init__(self):

        self.opponent_ip = None
        self.opponent_username = None
        self.setup = True


        self.new_move = False
        self.move = None



    #ACTUAL
    def send(self, move: str):
        print(self.opponent_ip)

        server = (self.opponent_ip, 4000)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        x = bytes(str(move), encoding='utf-8')

        while True:
            s.sendto(x, server)
            return


    def recv(self):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((str(socket.gethostbyname(socket.gethostname())), 4000))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print('host actual: waiting for connection')

            while True:
                data, addr = s.recvfrom(1024)
                print('host actual: connection established, data received')
                data = str(data.decode('utf-8'))

                self.move = data
                self.new_move = True
                return

    
    #SETUP
    def user_setup(self, username, code):
        server_ip = str(netaddr.IPAddress(int(code)))
        self.opponent_ip = server_ip

        host = str(socket.gethostbyname(socket.gethostname()))
        port = 4005

        server = (server_ip, 4000)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))
        x = bytes(str(username), encoding='utf-8') #encodes the move

        while True:
            s.sendto(x, server)
            return
        
    
        
    def host_setup(self):
        host = str(socket.gethostbyname(socket.gethostname())) #own ip
        port = 4000
        
        
        print('Code: ', int(netaddr.IPAddress(str(socket.gethostbyname(socket.gethostname())))))



        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('host setup: waiting for connection')

        while True:
            data, addr = s.recvfrom(1024)
            print('connection established; data saved')
            self.opponent_ip = addr[0]  
            self.opponent_username = str(data.decode('utf-8'))
            print(self.opponent_username)
            return


    def set_opponent_ip(self, code):
        self.opponent_ip = str(netaddr.IPAddress(code))