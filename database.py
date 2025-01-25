import json

server_dict = dict()
categories = dict()

DEFAULT_CATEGORY = "global"

def add_server_list(chatId, server, name):
    server_list = server_dict.get(str(chatId), {})
    
    if server not in server_list.keys():
        server_info = {
            "name" : name, 
            "category" : DEFAULT_CATEGORY
        }
        server_dict[str(chatId)] = {server : server_info}
    
def delete_server_from_list(chatId, server):
    server_list = server_dict.get(str(chatId), {})

    if(server in server_list.keys()):
        server_list.pop(server)
        return True
    
    elif(get_server_by_name(chatId, server)):
        server_list.pop(get_server_by_name(chatId, server))
        return True

    return False

def get_server_list(chatId):
    return server_dict.get(str(chatId), {}).keys()

def set_server_name(chatId, server, name):
    try:
        server_dict.get(str(chatId), {})[server]['name'] = name
    except KeyError:
        return False

def get_server_name(chatId, server):
    try:
        return server_dict.get(str(chatId), {})[server]['name']
    except:
        return False
    
def get_server_by_name(chatId, name):
    server_list = server_dict.get(str(chatId), {})
    for i in server_list:
        if server_list[i]['name'] == name:
            return i
        
    return False

def set_server_category(chatId, server, category):
    try:
        server_dict.get(str(chatId), {})[server]['category'] = category
        return True
    except KeyError:
        return False

def get_server_category(chatId, server):
    try:
        return server_dict.get(str(chatId), {})[server]['category']
    
    except KeyError:
        return None

def set_categories(chatId):
    try:
        global categories
        server_list = server_dict.get(str(chatId), {})
        for server, info in server_list.items():
            category = info['category']
            create_new_category(chatId, category)
    except:
        return False
    
def get_categories(chatId):
    try:
        return categories.get(str(chatId), [])
    except:
        return None

def create_new_category(chatId, category):
    try:
        global categories
        if category not in categories[str(chatId)]:
            categories[str(chatId)].append(category)
            return True
        else:
            return False
        
    except:
        categories[str(chatId)] = [category]
        return True

def delete_category_from_lists(chatId, category):
    try:
        global categories, server_dict
        flag = False
        idd = str(chatId)
        for i in range(len(categories[idd])):
            if categories[idd][i] == category:
                flag = True
                categories[idd].pop(i)

        if not flag:
            return False
        
        server_list = server_dict.get(idd, {})
        for i in server_list:
            if server_list[i]['category'] == category:
                server_list[i]['category'] = DEFAULT_CATEGORY

        return True
    
    except:
        return False
    
def get_servers_with_category(chatId, category):
    try:
        server_list = get_server_list(chatId)
        if(category == DEFAULT_CATEGORY): return server_list
        else:
            return [i for i in server_list if get_server_category(chatId, i) == category]
        
    except:
        return None

def load_categories():
    for i in server_dict.keys():
        set_categories(i)

def json_putInfo():
    with open('datas.json', 'w') as f:
        json.dump(server_dict, f, indent=4)

def json_loadInfo():
    try:
        with open('datas.json', 'r') as f:
            global server_dict
            server_dict = json.load(f)
            load_categories()
    except:
        json_putInfo()