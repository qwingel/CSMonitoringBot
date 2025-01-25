import os
import telebot
from telebot import types
from dotenv import load_dotenv
from time import sleep
from database import *
from server import get_server, get_players


load_dotenv()
token = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello!\nUse /addserver <server address>\nto get server information\nType /help for see more info')

@bot.message_handler(commands = ['addserver', 'new'])
def add_server(message):
    try:
        cmd, ip = message.text.split()
    except:
        bot.send_message(message.chat.id, 'Check the message format.\nFor example:\n/addserver 46.174.52.184:27015')
        return
    
    server = get_server(ip)
    if not server:
        bot.send_message(message.chat.id, ip + ' > is not avaible')

    else:
        name = server.server_name
        add_server_list(message.chat.id, ip, name)
        bot.send_message(message.chat.id, name + ' added to the server list')
        showReplyButtons(message.chat.id)


@bot.message_handler(commands = ['list', 'servers'])
def info_list(message):
    lst_servers = get_server_list(message.chat.id)
    if not lst_servers:
        bot.send_message(message.chat.id, 'You have no one server in list.\nUse /addserver <server address>')
        return
    
    msgg = ''
    count = 0

    for i in lst_servers:
        count += 1
        server = get_server(i)
        if not server:
            msgg += f'\n {count}. {i} > is not avaible'
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
        bot.send_message(message.chat.id, 'Check the message format.\nFor example:\n/delserver 46.174.52.184:27015\n/delserver [Beauty] >> Hide-and-Seek public')
        return
    
    if(delete_server_from_list(message.chat.id, server_id)):
        bot.send_message(message.chat.id, f'Server {server_id} was delete')
        showReplyButtons(message.chat.id)

    else:
        bot.send_message(message.chat.id, f'Server {server_id} not found')
            
@bot.message_handler(commands=['category', 'createcategory'])
def new_category(message):
    try:
        cmd, category = message.text.split(' ', 1)
    except:
        bot.send_message(message.chat.id, 'Check the message format.\nFor example:\n/category KZ\n')
        return
    
    if create_new_category(message.chat.id, category):
        bot.send_message(message.chat.id, f'Category {category} was created')
    else:
        bot.send_message(message.chat.id, f'Category {category} is already exists')

@bot.message_handler(commands=['setcategory'])
def set_category(message):
    if get_categories(message.chat.id) is None:
        bot.send_message(message.chat.id, "You don't have any categories. Use /category <category_name>")
        return

    global addServerToCategory, showCategoryReplyButton
    addServerToCategory = True
    showCategoryReplyButton = True
    bot.send_message(message.chat.id, "Select the category in which you want to add the server")
    showReplyButtons(message.chat.id)

@bot.message_handler(commands=['delcategory'])
def delete_category(message):
    if get_categories(message.chat.id) is None:
        bot.send_message(message.chat.id, "You don't have any categories. Use /category <category_name>")
        return
    
    try:
        cmd, category = message.text.split(' ', 1)
    except:
        bot.send_message(message.chat.id, 'Check the message format.\nFor example:\n/delcategory KZ\n')
        return
    
    if category != DEFAULT_CATEGORY and delete_category_from_lists(message.chat.id, category):
        bot.send_message(message.chat.id, f'Category {category} was deleted')
    else:
        bot.send_message(message.chat.id, f'Category {category} is not exists')
    


@bot.message_handler(commands=['help', 'info'])
def show_help(message):
    msgg =f'<b>\
/addserver(/new) ip:port - add server to the your list</b>\n\
<b>/list(/servers) - show your list of servers</b>\n\
<b>/delserver(/delete) Name or ip:port - delete server from your list</b>\n\
<b>/category(/createcategory) category name - set the category for the server</b>\n\
<b>/setcategory - choose category for server</b>\n\
<b>/delcategory - delete your category</b>'
    bot.send_message(message.chat.id, msgg, parse_mode='html')

@bot.message_handler(content_types=['text'])
def message_handler(message):
    text = message.text
    ip = get_server_by_name(message.chat.id, text)
    categ = get_categories(message.chat.id)
    global last_category, addServerToCategory
    if ip:
        if addServerToCategory:
            if set_server_category(message.chat.id, ip, last_category):
                bot.send_message(message.chat.id, f'Server {text} added to the {last_category} category')
                last_category = 'global'
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
    
    elif text == 'Back':
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
            msgg = 'Choose category'
            for i in lst_categories:
                if i != DEFAULT_CATEGORY:
                    markup.add(types.KeyboardButton(i))

            markup.add(types.KeyboardButton(DEFAULT_CATEGORY))
    else:
        msgg = 'Choose server'
        servers = get_servers_with_category(chatId, category)
        for i in servers:
            name = get_server_name(chatId, i)
            if name:
                markup.add(types.KeyboardButton(name))

        markup.add(types.KeyboardButton('Back'))

    bot.send_message(chatId, msgg, reply_markup=markup)

if __name__ == '__main__':
    json_loadInfo()
    showCategoryReplyButton = True
    addServerToCategory = False
    last_category = DEFAULT_CATEGORY
    print('TeleBot is starting...')
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            json_putInfo()
            sleep(0.3)