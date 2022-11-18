import translators as ts

token = "5758116360:AAEgAFe9S7CDuSyiMOm7XODn0gfmcPaqyc8"

language = """
Choose a language🇺🇸
Tilni tanlang🇺🇿
Выберите язык🇷🇺
"""


def com(lang):
    return f"""
{ts.google("I can help you to get meanings of words and many other things. If you're new in the EDBot I'll help you.", to_language=lang)}
{ts.google("You can control me by sending these commands:", to_language=lang)}

/create-{ts.google("for creating a new docx document.It is useful when you want to save all the words that you search", to_language=lang)}
/dict-{ts.google("this command help you to find meaning, synonym, antonym, translation of the word that you write", to_language=lang)}
/menu-{ts.google("for opening menubar: Settings, Editing Profile and etc", to_language=lang)}
/commands-{ts.google("this command will list all the commands you need to control the bot", to_language=lang)}
/get_doc-{ts.google("this command return you a finished version of the docx document that you created before to save the words that you search", to_language=lang)}
/get_instruction-{ts.google("to get the instruction", to_language=lang)}
/get_translation-{ts.google("for only translating the word or sentence", to_language=lang)}"""


asking_phone = """Telefon raqamingizni yuborish uchun tugmani bosing"""
