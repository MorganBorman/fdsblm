prefix = "smf_"

table_names = {}

table_names['Member']               = 'members'
table_names['MemberGroup']          = 'membergroups'
table_names['Theme']                = 'themes'
table_names['IpName']               = 'sb_srv_ipnames'
table_names['PunitiveEffect']       = 'sb_srv_punitive_effects'
table_names['Demo']                 = 'sb_srv_demos'
table_names['DemoTag']              = 'sb_srv_demo_tags'

for key in table_names.keys():
    table_names[key] = prefix + table_names[key]

