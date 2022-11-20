from gtts import gTTS
import telebot
import logging
import translators as ts
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from MP3_downloader_saver import scrape
from PGAdmin import checking_user
from PGAdmin.connect import getting_language, load_data
from PyDocX import delete1
from Telebot.Bot_functions import ikm_language, get_name, get_doc_name_and_create_doc, ikm_todo, send, ikm_save, finish
from Telebot.Bot_texts import token, language, com
from Telebot.Bot_utils import returner_, check_word_spelling, get_dict
from PyDict import Pydict

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot = telebot.TeleBot(token)
data_dict = {}
word = ''
lang = ''
list_ = [False, False, False, False]
counter = [0, 0, 0, 0]
word_l = {}


def running(w):
    if not scrape(w):
        tts = gTTS(text=w, lang='en-gb')
        tts.save('C:/Users/abdul/PycharmProjects/PyDict_TeleBot/MP3_downloader_saver/' + w + '.mp3')
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
    datum = returner_(message)
    if not datum:
        bot.send_message(chat_id=message.chat.id,
                         text=language,
                         reply_markup=ikm_language())
    else:
        global lang
        lang = datum
        bot.send_message(chat_id=message.chat.id,
                         text=ts.google(query_text="Yaratmoqchi bo'lgan documentga nom bering",
                                        to_language=datum))
        bot.register_next_step_handler(message, get_doc_name_and_create_doc, data_dict, logger, bot, datum)


def ecs(message):
    if message.text == 'Yes':
        bot.send_message(chat_id=message.chat.id,
                         text=ts.google(query_text="So'zning lug'atini chiqazib berish toxtatildi",
                                        to_language=lang),
                         reply_markup=ReplyKeyboardRemove()
                         )
        bot.send_message(chat_id=message.chat.id,
                         text=com(lang))
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=ts.google(query_text="Iltimos so'zni qaytatdan kiriting",
                                        to_language=lang),
                         reply_markup=ReplyKeyboardRemove()
                         )
        bot.register_next_step_handler(message, dictio)


def dictio(message):
    spell = check_word_spelling(message.text)
    global word
    if spell is True:
        word = message.text
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
    elif len(spell) != 0 and type(spell) is str:
        text1 = f"*{message.text}* so'ziga o'xshash so'z: "
        bot.send_message(chat_id=message.chat.id,
                         text=ts.google(query_text="Siz so'zni noto'g'ri kiritdingiz",
                                        to_language=lang)
                         )
        bot.send_message(chat_id=message.chat.id,
                         text=ts.google(query_text=text1,
                                        to_language=lang) + f' *{spell}*',
                         parse_mode='Markdown'
                         )
        text1 = ts.google(query_text="So'zni kiriting yoki ", to_language=lang)
        text2 = ts.google(query_text="commandasini yuboring", to_language=lang)
        text = text1 + ' /ecs ' + text2
        bot.send_message(chat_id=message.chat.id,
                         text=text)
        bot.register_next_step_handler(message, dictio)
    elif spell == 'True_command_True':
        text1 = ts.google(query_text="So'zni kiriting yoki ", to_language=lang)
        text2 = ts.google(query_text="commandasini yuboring", to_language=lang)
        text = text1 + ' /ecs ' + text2
        bot.send_message(chat_id=message.chat.id,
                         text=text)
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
        text1 = ts.google(query_text="So'zni kiriting yoki ", to_language=lang)
        text2 = ts.google(query_text="commandasini yuboring", to_language=lang)
        text = text1 + ' /ecs ' + text2
        bot.send_message(chat_id=message.chat.id,
                         text=text)
        bot.register_next_step_handler(message, dictio)


@bot.callback_query_handler(func=lambda call: call.data in ('save', 'continue', 'speak'))
def get_act(call):
    if call.data == 'save':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=ts.google(
                                  query_text="Quyidagilardan qaysi birlari documentda bo'lishi kerakligini tanlang",
                                  to_language=lang),
                              message_id=call.message.message_id,
                              reply_markup=ikm_save(list_))
    elif call.data == 'speak':
        running(word)
        send(call.message, bot, word)
    elif call.data == 'continue':
        text1 = ts.google(query_text="So'zni kiriting yoki ", to_language=lang)
        text2 = ts.google(query_text="commandasini yuboring", to_language=lang)
        text = text1 + ' /ecs ' + text2
        bot.send_message(chat_id=call.message.chat.id,
                         text=text)
        bot.register_next_step_handler(call.message, dictio)


def preparing_word_list():
    a = Pydict('yellow')
    mean = a.meaning()
    translation = a.translate('uz')
    synonym = a.getSynonyms()
    antonym = a.getAntonyms()
    list_mean = []
    txt_anton = ""
    txt_syno = ""
    for i in range(2):
        if i == 0:
            for j in synonym:
                txt_syno += f'{j}, '
        else:
            for j in antonym:
                txt_anton += f'{j}, '
    for i in range(len(list(mean.keys()))):
        txt = f"{list(mean.keys())[i]}: {list(mean.values())[i][0]}; "
        list_mean.append(txt)
    word_l['yellow'] = [
        {'Meaning': list_mean if list_[0] is True else word_l.pop('Meaning'),
         'Translation': translation if list_[1] is True else word_l.pop('Translation'),
         'Synonym': txt_syno if list_[2] is True else word_l.pop('Synonym'),
         'Antonym': txt_anton if list_[3] is True else word_l.pop('Antonym')
         }]


@bot.callback_query_handler(
    func=lambda call: call.data in ('definition', 'translation', 'synonym', 'antonym', 'finish'))
def get_some(call):
    caller = call.data
    if caller == 'definition':
        list_[0] = True if counter[0] == 0 else False
        counter[0] = 1 if list_[0] is True else 0
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=ts.google(
                                  query_text="Quyidagilardan qaysi birlari documentda bo'lishi kerakligini tanlang",
                                  to_language=lang),
                              message_id=call.message.message_id,
                              reply_markup=ikm_save(list_))
    elif caller == 'translation':
        list_[1] = True if counter[1] == 0 else False
        counter[1] = 1 if list_[1] is True else 0
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=ts.google(
                                  query_text="Quyidagilardan qaysi birlari documentda bo'lishi kerakligini tanlang",
                                  to_language=lang),
                              message_id=call.message.message_id,
                              reply_markup=ikm_save(list_))
    elif caller == 'synonym':
        list_[2] = True if counter[2] == 0 else False
        counter[2] = 1 if list_[2] is True else 0
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=ts.google(
                                  query_text="Quyidagilardan qaysi birlari documentda bo'lishi kerakligini tanlang",
                                  to_language=lang),
                              message_id=call.message.message_id,
                              reply_markup=ikm_save(list_))
    elif caller == 'antonym':
        list_[3] = True if counter[3] == 0 else False
        counter[3] = 1 if list_[3] is True else 0
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=ts.google(
                                  query_text="Quyidagilardan qaysi birlari documentda bo'lishi kerakligini tanlang",
                                  to_language=lang),
                              message_id=call.message.message_id,
                              reply_markup=ikm_save(list_))
    elif caller == 'finish':
        preparing_word_list()
        b = data_dict.keys()
        if 'docx_name' not in b:
            txt1 = ts.google(
                query_text="Siz hali so'zlarni qo'shish uchun document yaratmagansiz. ",
                to_language=lang
            )
            txt2 = ts.google(
                query_text=" commandasini yangi document yaratish uchun yuboring",
                to_language=lang
            )
            txt = txt1 + '/create' + txt2
            bot.send_message(chat_id=call.message.chat.id,
                             text=txt)
        else:
            finish(call.message, bot, data_dict['docx_name'], lang, word_l)


@bot.message_handler(['get_doc'])
def get_doc(message):
    if "docx_name" in list(data_dict.keys()):
        bot.send_document(chat_id=message.chat.id,
                          document=open(f'C:/Users/abdul/PycharmProjects/PyDict_TeleBot/Telebot/{data_dict["docx_name"]}.docx',
                                    'rb'))
        delete1(f'{data_dict["docx_name"]}.docx')
    else:
        txt = ts.google(query_text="Sizda hali yaratilgan document yo'q", to_language=lang)
        bot.send_message(chat_id=message.chat.id,
                         text=txt)


bot.polling()
