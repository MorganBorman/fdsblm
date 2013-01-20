import socket

class MumbleTeamConnection(object):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.connect()
        
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.hostname, self.port))
        except socket.error:
            pass
    
    def send(self, msg):
        tries = 0
        while tries < 3:
            try:
                totalsent = 0
                msglen = len(msg)
                while totalsent < msglen:
                    print "sending:", msg[totalsent:]
                    sent = self.socket.send(msg[totalsent:])
                    print sent
                    if sent == 0:
                        raise socket.error("error")
                        totalsent = 0
                    totalsent += sent
                return
            except socket.error:
                self.connect()
                if tries > 3:
                    print "Failed to send message to mumble autoteam server."
                    return
                else:
                    print "Failed to send message to mumble autoteam server. trying again..."
            tries += 1
    
    def changeteam(self, uid, server_name, team_name):
        self.send("changeteam {} {} {}\n".format(uid, server_name, team_name))
