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
            print "Established connection to mumble teams daemon."
        except socket.error:
            pass
    
    def send(self, msg):
        tries = 0
        while tries < 3:
            try:
                result = self.socket.sendall(msg)
                if result is None:
                    print "Successfully sent message: {}".format(repr(msg))
                    return
                else:
                    print "Got non None response from socket.sendall:", repr(result)
            except socket.error:
                print "Failed to send message to mumble autoteam server. trying again..."
                print "Reconnecting..."
                self.connect()
                    
            tries += 1
            
        print "Failed to send message to mumble autoteam server. Could not succeed in 3 tries."
    
    def changeteam(self, uid, server_name, team_name):
        self.send("changeteam {} {} {}\n".format(uid, server_name, team_name))
