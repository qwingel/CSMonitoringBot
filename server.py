import a2s

def get_server(address):
    try: return a2s.info(get_server_tuple(address))
    except: return False

def get_players(address):
    try: 
        players = a2s.players(get_server_tuple(address))
        return format_players_info(players)
    except: return False

def get_server_tuple(address):
    host, port = address.split(':')
    return (host, int(port))

def format_players_info(players):
    msgg = ''
    count = 0
    for i in players:
        count += 1
        time = formattime(int(i.duration))
        msgg += f'{count}. {i.name}   {time}\n'

    return msgg

def formattime(time):
    if time < 60:
        return f'{time} s.'
    
    if time < 3600:
        return f'{time // 60} m. {time % 60} s.'
    
    if time < 86400:
        return f'{time // 3600} h. {time % 3600 // 60} m. {time % 60} s.'
    
    return f'{time // 86400} d. {time % 86400 // 3600} h. {time % 3600 // 60} m. {time % 60} s.'