from textblob import Word
from PGAdmin import checking_user
from PGAdmin.connect import getting_language
from PyDict import Pydict


def check_word_spelling(word: str):
    if not word.startswith('/'):
        word = Word(word)
        result = word.spellcheck()

        if word == result[0][0]:
            return True
        else:
            return result[0][0]
    elif word == '/ecs':
        return False
    else:
        return 'True_command_True'


def get_dict(message, language):
    num = 1
    text = f"*Word*: {message.text}\n"
    a = Pydict(message.text)
    text += '\n*Meaning*: '
    dic = a.meaning()
    if len(dic) == 0:
        text += "This word has no meaning"
    else:
        for key, value in dic.items():
            text += '\n\t' + f"_{key}_" + ': '
            for s in value:
                text += s + '; '
    text += '\n\n*Synonyms*: \t'
    syn = a.getSynonyms()
    if len(syn) == 0:
        text += "This word has no synonyms"
    else:
        for i in syn:
            if num < 3:
                text += i + ', '
            elif num == 3:
                text += i
            num += 1
    num = 1
    text += '\n\n*Antonyms*: \t'
    anton = a.getAntonyms()
    if len(anton) == 0:
        text += "This word has no antonyms"
    else:
        for j in anton:
            if num < 3:
                text += j + ', '
            elif num == 3:
                text += j
            num += 1
    text += f'\n\n*Translation*: {a.translate(to_language=language)}'
    return text


def returner_(message):
    d = checking_user(message.chat.id)
    if d:
        return getting_language(message.chat.id)
    else:
        return False
