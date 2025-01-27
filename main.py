from index import *

load_dotenv()
token = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['start'])
def start(message):
    set_user_language(message.chat.id)
    bot.send_message(message.chat.id, get_phrase(get_user_language(message.chat.id), 'greeting'))

@bot.message_handler(commands = ['addserver', 'new'])
def add_server(message):
    lst_split = message.text.split()
    length = len(lst_split)
    if length == 2:
        cmd, ip = lst_split
    elif length == 3:
        cmd, ip, category = lst_split
    else:
        bot.send_message(message.chat.id, get_phrase(get_user_language(message.chat.id), 'format_example'))
        return
    
    server = get_server(ip)
    if not server:
        bot.send_message(message.chat.id, ip + get_phrase(get_user_language(message.chat.id), 'unavailable'))

    else:
        name = server.server_name
        add_server_list(message.chat.id, ip, name)
        if category:
            create_new_category(message.chat.id, category)
            set_server_category(message.chat.id, ip, category)

        bot.send_message(message.chat.id, name + get_phrase(get_user_language(message.chat.id), 'added_to_list'))
        showReplyButtons(message.chat.id)


@bot.message_handler(commands = ['list', 'servers'])
def info_list(message):
    lst_servers = get_server_list(message.chat.id)
    if not lst_servers:
        bot.send_message(message.chat.id, get_phrase(get_user_language(message.chat.id), 'no_servers'))
        return
    
    msgg = ''
    count = 0

    for i in lst_servers:
        count += 1
        server = get_server(i)
        if not server:
            msgg += f'\n {count}. {i} {get_phrase(get_user_language(message.chat.id), "unavailable")}'
        else:
            name = server.server_name
            players = server.player_count
            max_players = server.max_players
            msgg += f'\n{count}. [{get_server_category(message.chat.id, i)}] {name} ({players}/{max_players})'

    bot.send_message(message.chat.id, msgg)
    showReplyButtons(message.chat.id)

@bot.message_handler(commands=['delserver', 'delete'])
def delete_server(message):
    try:
        cmd, server_id = message.text.split(' ', 1)
    except:
        bot.send_message(message.chat.id, get_phrase(get_user_language(message.chat.id), 'delserver_format_example'))
        return
    
    if(delete_server_from_list(message.chat.id, server_id)):
        bot.send_message(message.chat.id, f'{get_phrase(get_user_language(message.chat.id), "server")} {server_id} {get_phrase(get_user_language(message.chat.id), "deleted")}')
        showReplyButtons(message.chat.id)

    else:
        bot.send_message(message.chat.id, f'{get_phrase(get_user_language(message.chat.id), "server")} {server_id} {get_phrase(get_user_language(message.chat.id), "not_found")}')
            
@bot.message_handler(commands=['category', 'createcategory'])
def new_category(message):
    try:
        cmd, category = message.text.split(' ', 1)
    except:
        bot.send_message(message.chat.id, get_phrase(get_user_language(message.chat.id), 'category_format_example'))
        return
    
    if create_new_category(message.chat.id, category):
        bot.send_message(message.chat.id, f'{get_phrase(get_user_language(message.chat.id), "category")} {category} {get_phrase(get_user_language(message.chat.id), "created")}')
    else:
        bot.send_message(message.chat.id, f'{get_phrase(get_user_language(message.chat.id), "category")} {category} {get_phrase(get_user_language(message.chat.id), "already_exists")}')

@bot.message_handler(commands=['setcategory'])
def set_category(message):
    if get_categories(message.chat.id) is None:
        bot.send_message(message.chat.id, get_phrase(get_user_language(message.chat.id), 'no_categories'))
        return

    global addServerToCategory, showCategoryReplyButton
    addServerToCategory = True
    showCategoryReplyButton = True
    bot.send_message(message.chat.id, get_phrase(get_user_language(message.chat.id), 'select_category'))
    showReplyButtons(message.chat.id)

@bot.message_handler(commands=['delcategory'])
def delete_category(message):
    if get_categories(message.chat.id) is None:
        bot.send_message(message.chat.id, get_phrase(get_user_language(message.chat.id), 'select_category_no_categories'))
        return
    
    try:
        cmd, category = message.text.split(' ', 1)
    except:
        bot.send_message(message.chat.id, get_phrase(get_user_language(message.chat.id), 'delcategory_format_example'))
        return
    
    if category != DEFAULT_CATEGORY and delete_category_from_lists(message.chat.id, category):
        bot.send_message(message.chat.id, f'{get_phrase(get_user_language(message.chat.id), "category")} {category}{get_phrase(get_user_language(message.chat.id), "deleted_category")}')
    else:
        bot.send_message(message.chat.id, f'{get_phrase(get_user_language(message.chat.id), "category")} {category} {get_phrase(get_user_language(message.chat.id), "not_exists")}')
    


@bot.message_handler(commands=['help', 'info'])
def show_help(message):
    msgg = get_phrase(get_user_language(message.chat.id), 'help')
    bot.send_message(message.chat.id, msgg, parse_mode='html')

@bot.message_handler(commands=['lang', 'language'])
def change_language(message):
    lang = RU if get_user_language(message.chat.id) == ENG else ENG
    set_user_language(message.chat.id, lang)
    bot.send_message(message.chat.id, get_phrase(get_user_language(message.chat.id), 'language'))

@bot.message_handler(content_types=['text'])
def message_handler(message):
    text = message.text
    ip = get_server_by_name(message.chat.id, text)
    categ = get_categories(message.chat.id)
    global last_category, addServerToCategory
    if ip:
        if addServerToCategory:
            if set_server_category(message.chat.id, ip, last_category):
                bot.send_message(message.chat.id, f'{get_phrase(get_user_language(message.chat.id), "server")} {text} {get_phrase(get_user_language(message.chat.id), "added_to_the")} {last_category} {get_phrase(get_user_language(message.chat.id), "category")}')
                last_category = DEFAULT_CATEGORY
                addServerToCategory = False
                showReplyButtons(message.chat.id)
        else:
            server = get_server(ip)
            name = server.server_name
            online = server.player_count - server.bot_count
            max_players = server.max_players
            server_map = server.map_name
            game = server.game
            players = get_players(ip)
            msgg =f'<b>\
{name}\n\
Map:</b> {server_map}\n\
<b>Mode:</b> {game}\n\
<b>Online:</b> {online}/{max_players}\n\n\
{players}\n\
Click to copy server ip\n\
<code>{ip}</code>'

            bot.send_message(message.chat.id, msgg, parse_mode='html')

    elif categ and text in categ:
        last_category = text
        global showCategoryReplyButton
        showCategoryReplyButton = False
        if addServerToCategory: 
            showReplyButtons(message.chat.id)
        else: 
            showReplyButtons(message.chat.id, last_category)
    
    elif text == get_phrase(get_user_language(message.chat.id), 'back'):
        showCategoryReplyButton = True
        showReplyButtons(message.chat.id)

    elif text == DEFAULT_CATEGORY:
        info_list(message)

def showReplyButtons(chatId, category=DEFAULT_CATEGORY):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    msgg = ''
    global showCategoryReplyButton
    if showCategoryReplyButton:
        lst_categories = get_categories(chatId)
        if lst_categories is None:
            showCategoryReplyButton = False
            showReplyButtons(chatId, category)
        else:
            msgg = get_phrase(get_user_language(chatId), 'choose_category')
            for i in lst_categories:
                if i != DEFAULT_CATEGORY:
                    markup.add(types.KeyboardButton(i))

            markup.add(types.KeyboardButton(DEFAULT_CATEGORY))
    else:
        msgg = get_phrase(get_user_language(chatId), 'choose_server')
        servers = get_servers_with_category(chatId, category)
        for i in servers:
            name = get_server_name(chatId, i)
            if name:
                markup.add(types.KeyboardButton(name))

        markup.add(types.KeyboardButton(get_phrase(get_user_language(chatId), 'back')))

    bot.send_message(chatId, msgg, reply_markup=markup)

def signal_handler(sig, frame):
    json_putInfo()
    SaveLanguages()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    json_loadInfo()
    LoadLanguages()
    showCategoryReplyButton = True
    addServerToCategory = False
    last_category = DEFAULT_CATEGORY
    print('TeleBot is starting...')
    # while True:
    #     try:
    bot.polling(none_stop=True)
        # except:
        #     json_putInfo()
        #     SaveLanguages()
        #     sleep(0.3)