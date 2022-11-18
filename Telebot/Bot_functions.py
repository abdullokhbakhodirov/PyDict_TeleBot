from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
import translators as ts
from MP3_downloader_saver import delete
from Telebot.Bot_texts import asking_phone, com


def ikm_language():
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton("English🇺🇸", callback_data='en'))
    ikm.add(InlineKeyboardButton("Uzbek🇺🇿", callback_data='uz'))
    ikm.add(InlineKeyboardButton("Russian🇷🇺", callback_data='ru'))
    return ikm


def ikm_todo(lang):
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton(text=ts.google(query_text='Save word to document 📄',
                                                to_language=lang),
                                 callback_data='save'))
    ikm.add(InlineKeyboardButton(text=ts.google(query_text='Pronounce of this word 🔊',
                                                to_language=lang),
                                 callback_data='speak'))
    ikm.add(InlineKeyboardButton(text=ts.google(query_text='Continue with another word',
                                                to_language=lang),
                                 callback_data='continue'))
    return ikm


def get_name(message, dictionary, bot, logger):
    name = message.text
    dictionary['Full name'] = name
    logger.info('Name added')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(ts.google(query_text="Telefon raqam 📞", to_language=dictionary['language']),
                                request_contact=True))
    bot.send_message(chat_id=message.chat.id,
                     text=ts.google(query_text=asking_phone, to_language=dictionary['language']),
                     reply_markup=keyboard)


def get_doc_name_and_create_doc(message, data_dict, logger, bot, lang):
    data_dict['docx_name'] = message.text
    logger.info('Docx file name saved')
    bot.send_message(chat_id=message.chat.id,
                     text=ts.google(query_text='Document muvaffaqiyatli yaratildi',
                                    to_language=lang))
    bot.send_message(chat_id=message.chat.id,
                     text=ts.google(query_text="Documentga so'z qo'shishni boshlash uchun /dict kommandasini yuboring",
                                    to_language=lang))


def send(message, bot, worde):
    bot.send_audio(chat_id=message.chat.id,
                   audio=open(f'C:/Users/abdul/PycharmProjects/PyDict_TeleBot/MP3_downloader_saver/{worde}.mp3',
                              'rb'))
    delete(f'{worde}.mp3')
