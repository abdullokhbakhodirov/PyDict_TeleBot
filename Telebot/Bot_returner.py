from gtts import gTTS
import telebot
import logging
import translators as ts
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

from MP3_downloader_saver import main
from MP3_downloader_saver.Downloader_saver.mp3_downloader import DIR_PATH
from PGAdmin import checking_user
from PGAdmin.connect import getting_language, load_data
from Telebot.Bot_functions import ikm_language, get_name, get_doc_name_and_create_doc, ikm_todo, ecs, send
from Telebot.Bot_texts import token, language, com
from Telebot.Bot_utils import returner_, check_word_spelling, get_dict

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot = telebot.TeleBot(token)
data_dict = {}
word = ''
lang = ''


def running(w):
    if not main(w):
        tts = gTTS(text=w, lang='en-gb')
        tts.save(f"{DIR_PATH}{w}.mp3")
        return 'Added'
    else:
        return True


@bot.message_handler(['start'])
def start(message):
    check = checking_user(message.chat.id)
    if not check:
        bot.send_message(chat_id=message.chat.id,
                         text=language,
                         reply_markup=ikm_language())
        logger.info("Successfully language chooser sent")
    else:
        a = getting_language(message.chat.id)
        global lang
        lang = a
        bot.send_message(chat_id=message.chat.id,
                         text=com(lang))


@bot.callback_query_handler(func=lambda call: len(call.data) == 2)
def get_lang(call):
    language_ = call.data
    if len(language_) == 2:
        data_dict['language'] = language_
    logger.info('Language added')
    bot.send_message(chat_id=call.message.chat.id,
                     text=ts.google(
                         query_text="Salom, biz sizga kim deb murojat qilsak bo'ladi?\nFamiliya va ismingizni yuboring",
                         to_language=language_))
    logger.info('Asking name has sent')
    bot.register_next_step_handler(call.message, get_name, data_dict, bot, logger)


@bot.message_handler(content_types=['contact'])
def get_phone(message):
    phone = message.contact.phone_number
    data_dict['Phone number'] = phone
    logger.info('Phone number added')
    load_data(data_dict, message.chat.id)
    logger.info('User successfully added')
    txt = com(data_dict['language'])
    global lang
    lang = data_dict['language']
    logger.info("Language is equaled to lang variable")
    bot.send_message(chat_id=message.chat.id,
                     text=txt,
                     reply_markup=ReplyKeyboardRemove())


@bot.message_handler(commands=['create'])
def creating_doc(message):
    check = checking_user(message.chat.id)
    if check:
        datum = getting_language(message.chat.id)
        global lang
        if len(lang) == 0:
            lang = datum
            bot.send_message(chat_id=message.chat.id,
                             text=ts.google(query_text="Yaratmoqchi bo'lgan documentga nom bering",
                                            to_language=datum))
            bot.register_next_step_handler(message, get_doc_name_and_create_doc, data_dict, logger, bot, datum)
        else:
            bot.send_message(chat_id=message.chat.id,
                             text=language,
                             reply_markup=ikm_language())


def dictio(message):
    spell = check_word_spelling(message.text)
    global word
    word = message.text
    if spell:
        text = get_dict(message, lang)
        bot.send_message(chat_id=message.chat.id,
                         text=text,
                         parse_mode='Markdown',
                         reply_markup=ikm_todo(lang))
    elif not spell:
        rkm = ReplyKeyboardMarkup(resize_keyboard=True)
        rkm.add(
            KeyboardButton(text="Yes"),
            KeyboardButton(text='No')
        )
        bot.send_message(chat_id=message.chat.id,
                         text=ts.google(query_text="Are you sure?",
                                        to_language=lang),
                         reply_markup=rkm
                         )
        bot.register_next_step_handler(message, ecs)
    elif spell == 'command':
        bot.send_message(chat_id=message.chat.id,
                         text=ts.google(
                             query_text="Iltimos boshqa commandalardan foydalanishdan oldin /ecs commandasini yuboring!",
                             to_language=lang))
        bot.register_next_step_handler(message, dictio)


@bot.message_handler(commands=['dict'])
def dicti(message):
    datum = returner_(message)
    if not datum:
        bot.send_message(chat_id=message.chat.id,
                         text=language,
                         reply_markup=ikm_language())
    else:
        global lang
        lang = datum
        bot.send_message(chat_id=message.chat.id,
                         text=ts.google(query_text="So'zni kiriting yoki /esc kommandasini yuboring",
                                        to_language=lang))
        bot.register_next_step_handler(message, dictio)


@bot.callback_query_handler(func=lambda call: call.data in ('save', 'continue', 'speak'))
def get_act(call):
    if call.data == 'save':
        ikm = InlineKeyboardMarkup()
        ikm.add(InlineKeyboardButton(text="Definition❌", callback_data='definition'),
                InlineKeyboardButton(text="Translation❌", callback_data='translation'))
        ikm.add(InlineKeyboardButton(text="Synonym❌", callback_data='synonym'),
                InlineKeyboardButton(text="Antonym❌", callback_data='antonym'))
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=ts.google(
                                  query_text="Quyidagilardan qaysi birlari documentda bo'lishi kerakligini tanlang",
                                  to_language=lang),
                              message_id=call.message.message_id,
                              reply_markup=ikm)
    elif call.data == 'speak':
        running(word)
        send(call.message, bot, word)
    elif call.data == 'continue':
        bot.send_message(chat_id=call.message.chat.id,
                         text=ts.google(query_text="So'zni kiriting yoki /esc kommandasini yuboring",
                                        to_language=lang))
        bot.register_next_step_handler(call.message, dictio)


bot.polling()
