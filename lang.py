import json
import yaml
import codecs

RU = 'ru'
ENG = 'en'

languages = dict()
phrases = dict()

def set_user_language(chatId, lang=ENG):
    global languages
    languages[str(chatId)] = lang

def get_user_language(chatId):
    try:
        return languages[str(chatId)]
    except:
        set_user_language(chatId)
        return get_user_language(chatId)
    
def get_phrase(lang, key):
    global phrases
    return phrases[lang][key]

def SaveLanguages():
    with open('lang.json', 'w') as f:
        json.dump(languages, f, indent=4)

def LoadLanguages():
    try:
        with open('lang.json', 'r') as f:
            global languages
            languages = json.load(f)
            
    except:
        SaveLanguages()

    LoadPhrases()

def LoadPhrases():
    global phrases
    lf = codecs.open( "lang.yaml", "r", "utf_8_sig")
    phrases = yaml.load(lf, Loader=yaml.FullLoader)