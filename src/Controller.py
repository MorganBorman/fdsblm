from AuthenticationModel import AuthenticationModel
from ServersModel import ServersModel
from SocketManager import SocketManager
from MumbleTeamConnection import MumbleTeamConnection
from PunitiveModel import PunitiveModel

from BaseTables import IpName

import time, datetime, sys, traceback

def cs_escape(string):
    """Replace any double quotes with single quotes."""
    return string.replace('\"', "''")

def format_date(epoch_seconds):
    date = datetime.datetime.fromtimestamp(epoch_seconds)
    
    now = time.time()
    
    if now-epoch_seconds > (60*60*24*2):
        return date.strftime("%Y/%m/%d")
    elif now-epoch_seconds > (60*60*24):
        return date.strftime("yesterday %H:%M")
    else:
        return date.strftime("%H:%M")

class Controller(object):
    commands = {}
    
    def __init__(self, master_ip, master_port, max_clients):
    
        self.authentication_model = AuthenticationModel()
        self.servers_model = ServersModel()
        self.socket_manager = SocketManager(master_ip, master_port, max_clients)
        self.mumbleteam_connection = MumbleTeamConnection("localhost", 28783)
        self.punitive_model = PunitiveModel()
        
        #######################################
        #connect up our signals
        #######################################
        
        #SocketManager
        
        self.socket_manager.started.connect(self.on_started)
        self.socket_manager.update.connect(self.on_update)
        self.socket_manager.stopped.connect(self.on_stopped)
        self.socket_manager.connect.connect(self.on_connect)
        self.socket_manager.request.connect(self.on_request)
        self.socket_manager.disconnect.connect(self.on_disconnect)
        
        #AuthenticationModel
        
        self.authentication_model.challenge.connect(self.on_auth_challenge)
        self.authentication_model.accept.connect(self.on_auth_accept)
        self.authentication_model.deny.connect(self.on_auth_deny)
        
        #PunitiveModel
        
        self.punitive_model.update.connect(self.on_effect_update)
        self.punitive_model.remove.connect(self.on_effect_remove)
        
        #######################################
        #start up the socket_manager
        #######################################
        
        self.socket_manager.run()
        
    def on_started(self, ip, port):
        print "Master server started."
        print "Listening on (%s, %s)." %(str(ip), str(port))
        print "Press Ctrl-c to exit."
        
    def on_update(self):
        self.punitive_model.refresh()
        
    def on_stopped(self):
        print "\nMaster server stopped."
        
    def on_connect(self, client):
        print "client connected %s" % str(client.address)
        
    def on_request(self, client, data):
        print "client command %s:" % str(client.address), data
        
        split_data = data.split(None, 1)
        split_data_len = len(split_data)
        
        if split_data_len < 1:
            return
        elif split_data_len < 2:
            command = split_data[0]
            arg_string = ""
        else:
            command, arg_string = split_data
            
        if command in self.commands:
            try:
                self.commands[command](self, client, arg_string)
            except:
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()    #@UnusedVariable
                sys.stderr.write("Uncaught exception occurred processing master client command.\n")
                sys.stderr.write(traceback.format_exc())
            
    
    def on_disconnect(self, client):
        self.servers_model.remove_server(client)
        print "client disconnected %s" % str(client.address)
    
    def on_auth_challenge(self, client, authid, challenge):
        message = "chalauth %s %s\n" % (authid, challenge)
        client.send(message)
    
    def on_auth_accept(self, client, authid, uid, display_name, groups):
        def remove_spaces(string):
            return string.translate(None, ' ')
            
        display_name = remove_spaces(display_name)
        groups = map(remove_spaces, groups)
        
        message = "succauth {} {} {} {}\n".format(authid, uid, display_name, ' '.join(groups))
        client.send(message)
    
    def on_auth_deny(self, client, authid):
        message = "failauth {}\n".format(authid)
        client.send(message)
        
    def on_effect_update(self, effect_id, effect_type, target_ip, target_mask, reason):
        message = "effectupdate {} {} {} {} {}\n".format(effect_id, effect_type, target_ip, target_mask, reason)
        self.servers_model.broadcast(message)
        
    def on_effect_remove(self, effect_id):
        message = "effectremove {}\n".format(effect_id)
        self.servers_model.broadcast(message)
        
def command(command_name):
    def dec(command_method):
        Controller.commands[command_name] = command_method
        return command_method
    return dec
        
@command("list")
def cmd_list(self, client, arg_string):
    servers_list = self.servers_model.get_server_list()
    client.send(servers_list)
    
@command("regserv")
def cmd_regserv(self, client, arg_string):
    args = arg_string.split()
    
    port = int(args[0])
    self.servers_model.register_server(client, port)
    client.send(self.punitive_model.get_effect_list())
    
@command("reqauth")
def cmd_reqauth(self, client, arg_string):
    args = arg_string.split()
    
    authid = int(args[0])
    member_name = args[1]
    self.authentication_model.request_authentication(client, authid, member_name)
    
@command("confauth")
def cmd_confauth(self, client, arg_string):
    args = arg_string.split()
    
    authid = int(args[0])
    response = args[1]
    self.authentication_model.confirm_authentication(client, authid, response)
    
@command("names")
def cmd_names(self, client, arg_string):
    args = arg_string.split()
    
    reqid = int(args[0])
    ip = int(args[1])
    mask = int(args[2])
    
    result_string_parts = []
    
    results = IpName.fetch(ip, mask)
    
    for result in results:
        result_string_parts.extend([cs_escape(result.name), format_date(result.date), result.count])
        
    result_string_parts = map(str, result_string_parts)
        
    result_string = '" "'.join(result_string_parts)
        
    client.send("names {} \"{}\"\n".format(reqid, result_string))
    
@command("recname")
def cmd_recname(self, client, arg_string):
    args = arg_string.split()
    
    name = args[0]
    ip = int(args[1])
    IpName.record(name, ip)

@command("disconnected")
def cmd_disconnected(self, client, arg_string):
    args = arg_string.split()
    
    uid = int(args[1])
    self.authentication_model.set_offline(client, uid)

@command("changeteam")
def cmd_changeteam(self, client, arg_string):
    args = arg_string.split()
    
    uid = int(args[0])
    server = args[1]
    team = args[2]
    self.mumbleteam_connection.changeteam(uid, server, team)

@command("addeffect")
def cmd_addeffect(self, client, arg_string):
    args = arg_string.split(" ", 9)

    effect_type = args[0]
    
    target_id = int(args[1])
    target_name = args[2]
    target_ip = int(args[3])
    target_mask = int(args[4])
    
    master_id = int(args[5])
    master_name = args[6]
    master_ip = int(args[7])
    
    expiry_time = int(args[8])
    
    reason = args[9]
    
    self.punitive_model.create_effect(client, 
                                      effect_type, 
                                      target_id, 
                                      target_name, 
                                      target_ip, 
                                      target_mask, 
                                      master_id, 
                                      master_name, 
                                      master_ip, 
                                      expiry_time, 
                                      reason)
    
@command("deleffect")
def cmd_deleffect(self, client, arg_string):
    args = arg_string.split()

    effect_id = int(args[0])
    self.punitive_model.remove_effect(effect_id)
