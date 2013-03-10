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

default_ircbot_enabled = True
doc = 'Enable connecting to the irc bot.'
ircbot_enabled = config_object.getOption('ircbot.enabled', default_ircbot_enabled, doc)=="True"

default_ircbot_ip = "localhost"
doc = 'What ip to connect to the irc bot on.'
ircbot_ip = config_object.getOption('ircbot.ip', default_ircbot_ip, doc)

default_ircbot_port = 28782
doc = 'What port to connect to the irc bot on.'
ircbot_port = int(config_object.getOption('ircbot.port', default_ircbot_port, doc))

del config_object

from Controller import Controller

controller = Controller(bind_ip, bind_port, backlog_size, mumbleteam_enabled, mumbleteam_ip, mumbleteam_port, ircbot_enabled, ircbot_ip, ircbot_port)
