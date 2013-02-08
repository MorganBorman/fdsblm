from config import config_object


default_bind_ip = "localhost"
doc = 'What interface to bind to.'
bind_ip = config_object.getOption('main.bind_ip', default_bind_ip, doc)

default_bind_port = 28787
doc = 'What port to bind to.'
bind_port = int(config_object.getOption('main.bind_port', default_bind_port, doc))

default_backlog_size = 5
doc = 'Max incoming connections to backlog.'
backlog_size = int(config_object.getOption('main.backlog_size', default_backlog_size, doc))

default_mumbleteam_enabled = True
doc = 'Enable connecting to the mumble team daemon.'
mumbleteam_enabled = config_object.getOption('mumbleteam.enabled', default_mumbleteam_enabled, doc)=="True"

default_mumbleteam_ip = "localhost"
doc = 'What ip to connect to the mumble team daemon on.'
mumbleteam_ip = config_object.getOption('mumbleteam.ip', default_mumbleteam_ip, doc)

default_mumbleteam_port = 28783
doc = 'What port to connect to the mumble team daemon on.'
mumbleteam_port = int(config_object.getOption('mumbleteam.port', default_mumbleteam_port, doc))

from Controller import Controller

controller = Controller(bind_ip, bind_port, backlog_size, mumbleteam_enabled, mumbleteam_ip, mumbleteam_port)
