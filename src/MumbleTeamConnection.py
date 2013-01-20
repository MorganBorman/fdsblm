import socket

class MumbleTeamConnection(object):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.connect()
        
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.hostname, self.port))
    
    def send(self, msg):
        tries = 0
        totalsent = 0
        msglen = len(msg)
        while totalsent < msglen:
            sent = self.socket.send(msg[totalsent:])
            if sent == 0:
                self.connect()
                self.totalsent = 0
                tries += 1
                if tries > 3:
                    print "Failed to send message to mumble autoteam server."
                    return
            totalsent += sent
    
    def changeteam(self, uid, server_name, team_name):
        self.send("changeteam {} {} {}\n".format(uid, server_name, team_name))
