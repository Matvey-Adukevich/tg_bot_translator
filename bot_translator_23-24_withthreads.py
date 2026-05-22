import requests
from bs4 import BeautifulSoup as b
import telebot
from telebot import types
import random
from requests_html import AsyncHTMLSession, HTMLSession
from threading import Thread
from icrawler.builtin import GoogleImageCrawler
from gtts import gTTS
from parser_collocations import parser_collocations
from parser_sentences import parser_sentences
# from parser_pictures import parser_pictures
# from parser_audio import parser_audio
#+pillow

session1 = AsyncHTMLSession()
session2 = HTMLSession()
session3 = HTMLSession()
bot = telebot.TeleBot('*Key*')
language = 'ru'
level = 'A1'
score = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text="Hello! Welcome to the bot! Use the command '/menu' to see the functions and to choose them! You can use  command '/help' to see all commands!")
    bot.send_message(message.chat.id, text="Здравствуйте! Добро пожаловать в бота! Используйте '/menu' чтобы увидеть функции бота и выбрать одну из них! Вы можете ввести '/help', чтобы увидеть краткое руководство по использованию данного бота!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    eng_button = types.KeyboardButton('/english (английский)')
    ru_button = types.KeyboardButton('/russian (русский)')
    markup.add(eng_button, ru_button)
    bot.send_message(message.chat.id, text="Пожалуйста, укажите язык для работы с ботом!\nPlease, choose language of the bot!", reply_markup=markup)

def programm():
    while True:
        try:
            URL_1 = 'https://www.dictionary.com/e/word-of-the-day/'
            URL_2 = 'https://www.dictionary.com/browse/'
            URL_3 = 'https://www.thesaurus.com/browse/'
            URL_4 = 'https://www.vocabulary.com/lists/186983'  # A1
            URL_5 = 'https://www.vocabulary.com/lists/186727'  # A2
            URL_6 = 'https://www.vocabulary.com/lists/187039'  # B1
            URL_7 = 'https://www.vocabulary.com/lists/187041'  # B2
            URL_8 = 'https://www.vocabulary.com/lists/8520574'  # C1
            URL_9 = 'https://www.vocabulary.com/lists/6202247'  # C2

            async def parsergame():
                global page_word_A1
                page_word_A1 = await session1.get(URL_4)
                global page_word_A2
                page_word_A2 = await session1.get(URL_5)
                global page_word_B1
                page_word_B1 = await session1.get(URL_6)
                global page_word_B2
                page_word_B2 = await session1.get(URL_7)
                global page_word_C1
                page_word_C1 = await session1.get(URL_8)
                global page_word_C2
                page_word_C2 = await session1.get(URL_9)
                # print(page_word_A1, page_word_A2, page_word_B1, page_word_B2, page_word_C1, page_word_C2)
                # print(page_word_A2)
                # print(page_word_B1)
                # print(page_word_B2)
                # print(page_word_C1)
                # print(page_word_C2)


            del_buttons = types.ReplyKeyboardRemove()
            session1.run(parsergame)

            def right_answer(message):
                if (message.text == "/menu"):
                    return menu(message)
                if (message.text in game_synonym):
                    if language == 'eng':
                        bot.send_message(message.chat.id, text='✅Right!✅', reply_markup=del_buttons)
                    elif language == 'ru':
                        bot.send_message(message.chat.id, text='✅Верно!✅', reply_markup=del_buttons)
                    if page_number == 1:
                        words_A1(message)
                    if page_number == 2:
                        words_A2(message)
                    if page_number == 3:
                        words_B1(message)
                    if page_number == 4:
                        words_B2(message)
                    if page_number == 5:
                        words_C1(message)
                    if page_number == 6:
                        words_C2(message)
                elif (message.text != game_synonym):
                    if language == 'eng':
                        bot.send_message(message.chat.id, text='❌Not that!❌')
                        choice = bot.send_message(message.chat.id, text='Your choice: ')
                    elif language == 'ru':
                        bot.send_message(message.chat.id, text='❌Не этот!❌')
                        choice = bot.send_message(message.chat.id, text='Ваш выбор: ')
                    bot.register_next_step_handler(choice, right_answer)

            def right_answer_test(message):
                if (message.text == "/menu"):
                    return menu(message)
                if (message.text in game_synonym):
                    print('Yes')
                    if language == 'eng':
                        bot.send_message(message.chat.id, text='✅Right!✅')
                    elif language == 'ru':
                        bot.send_message(message.chat.id, text='✅Верно!✅')
                    testing(message)
                elif (message.text != game_synonym):
                    global mistakes
                    mistakes = mistakes + 1
                    if language == 'eng':
                        bot.send_message(message.chat.id, text='❌Not that!❌')
                        choice = bot.send_message(message.chat.id, text='Your choice: ')
                    elif language == 'ru':
                        bot.send_message(message.chat.id, text='❌Не этот!❌')
                        choice = bot.send_message(message.chat.id, text='Ваш выбор: ')
                    bot.register_next_step_handler(choice, right_answer_test)

            def ant_syn_word():
                print('7')
                if page_number == 1:
                    page_word = requests.get(URL_3 + str(word_A1))
                if page_number == 2:
                    page_word = requests.get(URL_3 + str(word_A2))
                if page_number == 3:
                    page_word = requests.get(URL_3 + str(word_B1))
                if page_number == 4:
                    page_word = requests.get(URL_3 + str(word_B2))
                if page_number == 5:
                    page_word = requests.get(URL_3 + str(word_C1))
                if page_number == 6:
                    page_word = requests.get(URL_3 + str(word_C2))
                print('9')
                soup = b(page_word.text, 'html.parser')
                synonyms_1 = soup.find_all(class_='Cil3vPqnHSU3LLCTZ62n Ip2xyQSEjrh_jZExawdC fQdXDP6Pfndr85gESLI_')
                synonyms_2 = soup.find_all(class_='Cil3vPqnHSU3LLCTZ62n Ip2xyQSEjrh_jZExawdC DL3p3OH7u8i4dIoN1agF')
                h = [e.text for e in synonyms_1]
                hb = [ui.text for ui in synonyms_2]
                print(h + hb)
                for i in hb:
                    if i not in h:
                        h.append(i)
                antonyms_1 = soup.find_all(class_='Cil3vPqnHSU3LLCTZ62n c2bTkbyZ6pxWgWJDxVMX GngaNNiSLAlPYOZdx7Ax')
                antonyms_2 = soup.find_all(class_='Cil3vPqnHSU3LLCTZ62n c2bTkbyZ6pxWgWJDxVMX VnK9FPYVTcphUnMI4CHa')
                c = [d.text for d in antonyms_1]
                f = [g.text for g in antonyms_2]
                print(c + f)
                for i in f:
                    if i not in c:
                        c.append(i)
                print(c)
                print('8')
                if h == [] or c == [] or len(c) < 3:
                    print('5')
                    if page_number == 1:
                        return A1()
                    if page_number == 2:
                        return A2()
                    if page_number == 3:
                        return B1()
                    if page_number == 4:
                        return B2()
                    if page_number == 5:
                        return C1()
                    if page_number == 6:
                        return C2()
                if h != [] and c != []:
                    global synonyms_rand_index
                    synonyms_rand_index = random.randint(0, len(h) - 1)
                    global antonyms_rand_index_1
                    antonyms_rand_index_1 = random.randint(0, len(c) - 1)
                    global antonyms_rand_index_2
                    antonyms_rand_index_2 = random.randint(0, len(c) - 1)
                    while antonyms_rand_index_2 == antonyms_rand_index_1:
                        antonyms_rand_index_2 = random.randint(0, len(c) - 1)
                    global antonyms_rand_index_3
                    antonyms_rand_index_3 = random.randint(0, len(c) - 1)
                    while antonyms_rand_index_3 == antonyms_rand_index_2 or antonyms_rand_index_3 == antonyms_rand_index_1:
                        antonyms_rand_index_3 = random.randint(0, len(c) - 1)
                    global game_synonym
                    game_synonym = h[synonyms_rand_index]
                    global game_antonyms_1
                    game_antonyms_1 = c[antonyms_rand_index_1]
                    global game_antonyms_2
                    game_antonyms_2 = c[antonyms_rand_index_2]
                    global game_antonyms_3
                    game_antonyms_3 = c[antonyms_rand_index_3]
                    print('Synonyms: ', game_synonym)
                    print('Antonyms: ', game_antonyms_1, ' ', game_antonyms_2, ' ', game_antonyms_3)
                    print(antonyms_rand_index_1, antonyms_rand_index_2, antonyms_rand_index_3)
                    print(c)
                    print('6')

            def A1():
                print('3')
                soup = b(page_word_A1.text, 'html.parser')
                array_A1 = soup.find_all('a', class_='word')
                A1_word = [i.text for i in array_A1]
                print(A1_word)
                random_index = random.randint(0, len(A1_word) - 1)
                global word_A1
                word_A1 = A1_word[random_index]
                print('4')
                ant_syn_word()

            def A2():
                soup_A2 = b(page_word_A2.text, 'html.parser')
                array_A2 = soup_A2.find_all('a', class_='word')
                A2_word = [i.text for i in array_A2]
                random_index = random.randint(0, len(A2_word) - 1)
                global word_A2
                word_A2 = A2_word[random_index]
                ant_syn_word()

            def B1():
                soup_B1 = b(page_word_B1.text, 'html.parser')
                array_B1 = soup_B1.find_all('a', class_='word')
                B1_word = [i.text for i in array_B1]
                random_index = random.randint(0, len(B1_word) - 1)
                global word_B1
                word_B1 = B1_word[random_index]
                ant_syn_word()

            def B2():
                soup_B2 = b(page_word_B2.text, 'html.parser')
                array_B2 = soup_B2.find_all('a', class_='word')
                B2_word = [i.text for i in array_B2]
                random_index = random.randint(0, len(B2_word) - 1)
                global word_B2
                word_B2 = B2_word[random_index]
                ant_syn_word()

            def C1():
                soup_C1 = b(page_word_C1.text, 'html.parser')
                array_C1 = soup_C1.find_all('a', class_='word')
                C1_word = [i.text for i in array_C1]
                random_index = random.randint(0, len(C1_word) - 1)
                global word_C1
                word_C1 = C1_word[random_index]
                ant_syn_word()

            def C2():
                soup_C2 = b(page_word_C2.text, 'html.parser')
                array_C2 = soup_C2.find_all('a', class_='word')
                C2_word = [i.text for i in array_C2]
                random_index = random.randint(0, len(C2_word) - 1)
                global word_C2
                word_C2 = C2_word[random_index]
                ant_syn_word()

            def result():
                global level
                global res
                if mistakes <= 2:
                    if language == 'eng':
                        res = 'Next level!'
                    elif language == 'ru':
                        res = 'Следующий уровень!'
                elif mistakes > 2:
                    if language == 'eng':
                        res = 'Try again!'
                    elif language == 'ru':
                        res = 'Попробуйте снова!'
                    level = 'A1'

            def testing(message):
                global mistakes
                global page_number
                global level
                global score
                if level == 'A1':
                    page_number = 1
                elif level == 'A2':
                    page_number = 2
                elif level == 'B1':
                    page_number = 3
                elif level == 'B2':
                    page_number = 4
                elif level == 'C1':
                    page_number = 5
                elif level == 'C2':
                    page_number = 6
                global trying_5
                trying_5 = trying_5 + 1
                if (trying_5 >= 11) or (mistakes>2):
                    result()
                    if res == 'Try again!' or res == 'Попробуйте снова!':
                        bot.send_message(message.chat.id, res)
                    elif res == 'Next level!' or res == 'Следующий уровень!':
                        score = str(10 - mistakes)
                        if language == 'eng':
                            bot.send_message(message.chat.id, 'You have '+score+' of 10 right words!')
                            bot.send_message(message.chat.id, 'You have '+level+' level!')
                        elif language == 'ru':
                            bot.send_message(message.chat.id, 'Вы набрали '+score+' из 10 возможных!')
                            bot.send_message(message.chat.id, 'У вас уровень языка '+level+'!')
                        if level != 'C2':
                            bot.send_message(message.chat.id, res)
                        if level == 'A1':
                            level = 'A2'
                            page_number = 2
                        elif level == 'A2':
                            level = 'B1'
                            page_number = 3
                        elif level == 'B1':
                            level = 'B2'
                            page_number = 4
                        elif level == 'B2':
                            level = 'C1'
                            page_number = 5
                        elif level == 'C1':
                            level = 'C2'
                            page_number = 6
                        elif level == 'C2':
                            level = 'Master'
                    score = 0
                    trying_5 = 0
                    mistakes = 0
                    testing(message)
                elif (trying_5 < 11) and (mistakes<=2):
                    if level == 'A1':
                        A1()
                    elif level == 'A2':
                        A2()
                    elif level == 'B1':
                        B1()
                    elif level == 'B2':
                        B2()
                    elif level == 'C1':
                        C1()
                    elif level == 'C2':
                        C2()
                    elif level == 'Master':
                        if language == 'eng':
                            bot.send_message(message.chat.id, text='You are the master of English!', reply_markup=del_buttons)
                        elif language == 'ru':
                            bot.send_message(message.chat.id, text='Вы являетесь носителем языка!', reply_markup=del_buttons)
                        menu(message)
                    location = random.randint(1, 4)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                    btn_syn = types.KeyboardButton(game_synonym)
                    btn_ant1 = types.KeyboardButton(game_antonyms_1)
                    btn_ant2 = types.KeyboardButton(game_antonyms_2)
                    btn_ant3 = types.KeyboardButton(game_antonyms_3)
                    back = types.KeyboardButton('/menu')
                    if location == 1:
                        markup.add(btn_syn, btn_ant1, btn_ant2, btn_ant3, back)
                    elif location == 2:
                        markup.add(btn_ant1, btn_syn, btn_ant2, btn_ant3, back)
                    elif location == 3:
                        markup.add(btn_ant1, btn_ant2, btn_syn, btn_ant3, back)
                    elif location == 4:
                        markup.add(btn_ant1, btn_ant3, btn_ant2, btn_syn, back)
                    if level == 'A1':
                        user_answer_wait = bot.send_message(message.chat.id, word_A1, reply_markup=markup)
                    elif level == 'A2':
                        user_answer_wait = bot.send_message(message.chat.id, word_A2, reply_markup=markup)
                    elif level == 'B1':
                        user_answer_wait = bot.send_message(message.chat.id, word_B1, reply_markup=markup)
                    elif level == 'B2':
                        user_answer_wait = bot.send_message(message.chat.id, word_B2, reply_markup=markup)
                    elif level == 'C1':
                        user_answer_wait = bot.send_message(message.chat.id, word_C1, reply_markup=markup)
                    elif level == 'C2':
                        user_answer_wait = bot.send_message(message.chat.id, word_C2, reply_markup=markup)
                    bot.register_next_step_handler(user_answer_wait, right_answer_test)

            def parser(URL):
                r = requests.get(URL)
                soup = b(r.text, 'html.parser')
                word_of_the_day_1 = soup.find_all('h1', class_='js-fit-text')
                x = [c.text for c in word_of_the_day_1]
                global word_of_the_day
                word_of_the_day = str(x[0])
                m = requests.get(URL_2 + word_of_the_day)
                soup = b(m.text, 'html.parser')
                word_day_def = soup.find_all('div', class_='ESah86zaufmd2_YPdZtq')
                definition_word_day = [c.text for c in word_day_def]
                global word_definition_day
                word_definition_day = str(definition_word_day[0])

            def parser_pictures(word_to_find1111):
                filters = dict(type='photo')
                crawler = GoogleImageCrawler(storage={'root_dir': '.'})
                crawler.crawl(keyword=word_to_find1111, max_num=1, overwrite=True, filters=filters)

            def parser_audio(word_to_find2):
                s = gTTS(word_to_find2)
                s.save(f'.//audio//{word_to_find2}_audio.mp3')

            def parser_collocations(wordtofind, c):
                try:
                    soup3 = b(c.text, 'html.parser')
                    word2 = soup3.find_all(class_='table table-striped table-bordered table-hover table-condensed')
                    gf = [d.text for d in word2]

                    for i in gf:
                        a = i

                    op = []
                    a = a.replace(wordtofind, '*')
                    a = a.split('\n')

                    for i in a:
                        if i != '':
                            op.append(i)

                    c = []

                    for i in op:
                        if i != '*':
                            c.append(i)
                        if i == '*':
                            c.append('\n')

                    g = ''

                    for i in c[6:]:
                        g = g + '_' + str(i)
                        g = g.replace('*', wordtofind)

                    kli = ''
                    g = g.split('\n')

                    for i in g:
                        if str(i).count('_') == 7:
                            kli = kli + '\n' + i

                    kli = kli.split('\n')
                    dr = []

                    for i in kli:
                        if i != '':
                            dr.append(i)

                    yt = []

                    for i in dr:
                        yt.append(i.split('_'))

                    rt = []  # collocations

                    for i in yt:
                        rt.append(i[1])

                    global collocations
                    collocations = rt
                    return collocations
                except:
                    return ''

            def parser_sentences(wordtofind, c):
                try:
                    soup3 = b(c.text, 'html.parser')
                    word2 = soup3.find_all(class_='table table-striped table-bordered table-hover table-condensed')
                    gf = [d.text for d in word2]

                    for i in gf:
                        a = i

                    oi = []
                    a = a.replace(wordtofind, '*')
                    a = a.split('\n')

                    for i in a:
                        if i != '':
                            oi.append(i)

                    c = []

                    for i in oi:
                        if i != '*':
                            c.append(i)
                        if i == '*':
                            c.append('\n')

                    g = ''

                    for i in c[6:]:
                        g = g + '_' + str(i)
                        g = g.replace('*', wordtofind)

                    kli = ''
                    g = g.split('\n')

                    for i in g:
                        if str(i).count('_') == 7:
                            kli = kli + '\n' + i

                    kli = kli.split('\n')
                    dr = []

                    for i in kli:
                        if i != '':
                            dr.append(i)

                    yt = []

                    for i in dr:
                        yt.append(i.split('_'))

                    rui = []  # sentences

                    for i in yt:
                        rui.append(i[4:7])

                    gt = []

                    for i in rui:
                        for u in i:
                            gt.append(u)

                    global sentences
                    sentences = gt[::3]
                    return sentences
                except:
                    return ''

            def translation_threads(mes):
                picpic = Thread(target=parser_pictures, args=(mes,))
                picpic.start()
                audaud = Thread(target=parser_audio, args=(mes,))
                mes = mes.lower()
                gel = session3.get(f'https://www.linguatools.de/kollokationen-en/bolls/?utf8=%E2%9C%93&lemmahits=100&query={mes}&commit=Search+Collocations%21')
                colcol = Thread(target=parser_collocations, args=(mes,gel,))
                sensen = Thread(target=parser_sentences, args=(mes, gel,))
                audaud.start()
                colcol.start()
                sensen.start()
                picpic.join()

            def translation(message):
                if message.text == '/menu':
                    return menu(message)
                r = requests.get(URL_2 + message.text)
                soup_1 = b(r.text, 'html.parser')
                translation_1 = soup_1.find_all('div', class_='ESah86zaufmd2_YPdZtq')
                a = [c.text for c in translation_1]
                if a == []:
                    if language == 'eng':
                        bot.send_message(message.chat.id, "Sorry, we can't find this word/collocation. Check your word and try again.")
                    elif language == 'ru':
                        bot.send_message(message.chat.id, text="Извините, мы не можем найти это слово/словосочетание. Проверьте его написание и попробуйте снова.")
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn1 = types.KeyboardButton("/menu")
                    markup.add(btn1)
                    if language == 'eng':
                        msg2 = bot.send_message(message.chat.id, text='Enter word:', reply_markup=markup)
                    elif language == 'ru':
                        msg2 = bot.send_message(message.chat.id, text='Введите слово:', reply_markup=markup)
                    bot.register_next_step_handler(msg2, translation)
                if a!=[]:
                    translation_threads(message.text)
                    # threading.Thread(target=parser_pictures, args=(message.text)).start()
                    m = requests.get(URL_3 + message.text)
                    soup_2 = b(m.text, 'html.parser')
                    synonyms_1 = soup_2.find_all(class_='Cil3vPqnHSU3LLCTZ62n Ip2xyQSEjrh_jZExawdC fQdXDP6Pfndr85gESLI_')
                    synonyms_2 = soup_2.find_all(class_='Cil3vPqnHSU3LLCTZ62n Ip2xyQSEjrh_jZExawdC DL3p3OH7u8i4dIoN1agF')
                    zn = [nh.text for nh in synonyms_1]
                    th = [th.text for th in synonyms_2]
                    syn_arr = zn + th
                    w = []
                    for i in syn_arr:
                        if i not in w:
                            w.append(i)
                    antonyms_1 = soup_2.find_all(class_='Cil3vPqnHSU3LLCTZ62n c2bTkbyZ6pxWgWJDxVMX GngaNNiSLAlPYOZdx7Ax')
                    antonyms_2 = soup_2.find_all(class_='Cil3vPqnHSU3LLCTZ62n c2bTkbyZ6pxWgWJDxVMX VnK9FPYVTcphUnMI4CHa')
                    h = [d.text for d in antonyms_1]
                    f = [g.text for g in antonyms_2]
                    j = h + f
                    ant_array = []
                    for i in j:
                        if i not in ant_array:
                            ant_array.append(i)
                    u = [f'<code>{i}</code>' for i in w]
                    o = [f'<code>{i}</code>' for i in ant_array]
                    short_syn = [f'<code>{i}</code>' for i in w[0:50]]
                    short_ant = [f'<code>{i}</code>' for i in ant_array[0:50]]
                    col = [f'<code>{i}</code>' for i in collocations[:20]]
                    sent = [i for i in sentences[:10]]
                    # col = [f'<code>{i}</code>' for i in collocations[:20]]
                    # sentences = parser_sentences(wordtofind, gel)
                    # sent = [i for i in sentences[:10]]
                    # parser_audio(message.text)
                    # collocations = parser_collocations(message.text)
                    # col = [f'<code>{i}</code>' for i in collocations[:20]]
                    print('Synonyms: ', w)
                    print('Antonyms: ', ant_array)
                    print(a)
                    print(len(w))
                    print(len(ant_array))
                    print(collocations)
                    print(sent)
                    if a!=[]:
                        img = open('000001.jpg', 'rb')
                        bot.send_photo(message.chat.id, img)
                        audio = open(f'.//audio//{message.text}_audio.mp3', 'rb')
                        bot.send_audio(message.chat.id, audio)
                        audio.close()
                        if language == 'eng':
                            bot.send_message(message.chat.id, message.text + " - " + (str(a[0])))
                            if len(w) > 50:
                                bot.send_message(message.chat.id, 'Synonyms: ' + ', '.join(short_syn) + '.', parse_mode='HTML')
                            if len(ant_array) > 50:
                                bot.send_message(message.chat.id, 'Antonyms: ' + ', '.join(short_ant) + '.', parse_mode='HTML')
                            if u != [] and len(u) <= 50:
                                bot.send_message(message.chat.id, 'Synonyms: ' + ', '.join(u) + '.', parse_mode='HTML')
                            elif u == []:
                                bot.send_message(message.chat.id, text='No synonyms.')
                            if o != [] and len(o) <= 50:
                                bot.send_message(message.chat.id, "Antonyms: " + ', '.join(o) + ".", parse_mode='HTML')
                            elif o == []:
                                bot.send_message(message.chat.id, text='No Antonyms.')
                            if col !=[]:
                                bot.send_message(message.chat.id, 'Collocations: ' + ', '.join(col), parse_mode='HTML')
                            elif col == []:
                                bot.send_message(message.chat.id, text='No collocations.')
                            if sent !=[]:
                                bot.send_message(message.chat.id, 'Sentences: ' + '; '.join(sent), parse_mode='HTML')
                            elif sent == []:
                                bot.send_message(message.chat.id, text='No sentences.')
                        elif language == 'ru':
                            bot.send_message(message.chat.id, message.text + " - " + (str(a[0])))
                            if len(w) > 50:
                                bot.send_message(message.chat.id, 'Синонимы: ' + ', '.join(short_syn) + '.', parse_mode='HTML')
                            if len(ant_array) > 50:
                                bot.send_message(message.chat.id, 'Антонимы: ' + ', '.join(short_ant) + '.', parse_mode='HTML')
                            if u != [] and len(u) <= 50:
                                bot.send_message(message.chat.id, 'Синонимы: ' + ', '.join(u) + '.', parse_mode='HTML')
                            elif u == []:
                                bot.send_message(message.chat.id, text='Синонимов нет.')
                            if o != [] and len(o) <= 50:
                                bot.send_message(message.chat.id, "Антонимы: " + ', '.join(o) + ".", parse_mode='HTML')
                            elif o == []:
                                bot.send_message(message.chat.id, text='Антонимов нет.')
                            if col != []:
                                bot.send_message(message.chat.id, 'Словосочетания: ' + ', '.join(col), parse_mode='HTML')
                            elif col == []:
                                bot.send_message(message.chat.id, text='Словосочетаний нет.')
                            if sent !=[]:
                                bot.send_message(message.chat.id, 'Предложения: ' + '; '.join(sent), parse_mode='HTML')
                            elif sent == []:
                                bot.send_message(message.chat.id, text='Предложений нет.')
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        btn1 = types.KeyboardButton("/menu")
                        markup.add(btn1)
                        if language == 'eng':
                            msg3 = bot.send_message(message.chat.id, text='Enter word:', reply_markup=markup)
                        elif language == 'ru':
                            msg3 = bot.send_message(message.chat.id, text='Введите слово:', reply_markup=markup)
                        bot.register_next_step_handler(msg3, translation)

            @bot.message_handler(commands=['language'])
            def change_language(message):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                eng_button = types.KeyboardButton('/english (английский)')
                ru_button = types.KeyboardButton('/russian (русский)')
                markup.add(eng_button, ru_button)
                bot.send_message(message.chat.id, text="Пожалуйста, укажите язык для работы с ботом!\nPlease, choose language of the bot!", reply_markup=markup)

            @bot.message_handler(commands=['russian'])
            def russian_language(message):
                bot.send_message(message.chat.id, text='Вы выбрали русский язык! Если хотите изменить его, то введите "/language"')
                global language
                language = 'ru'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton('/menu')
                markup.add(back)
                bot.send_message(message.chat.id, text='Перейти в меню?', reply_markup=markup)

            @bot.message_handler(commands=['english'])
            def english_language(message):
                bot.send_message(message.chat.id, text='You chose english language! If you want to change, then enter "/language"')
                global language
                language = 'eng'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton('/menu')
                markup.add(back)
                bot.send_message(message.chat.id, text='Go to the menu?', reply_markup=markup)

            @bot.message_handler(commands=['help'])
            def choose(message):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("/menu")
                markup.add(btn1)
                print(language)
                if language == 'eng':
                    bot.send_message(message.chat.id, text="1)Bot has the main command '/menu' to choose or set the functions. \n2)If you want to change language, then enter '/language'.\n3)You can copy any word in translation after using this function, just click on it(left button of mouse)!\n4)Functions:\n-Word of the day (Слово дня) - every day bot send you a new word\n-Translate words (Перевод слов) - find meaning of the word, synonyms and antonyms of its\n-Game Synonyms and Antonyms (Игра синонимы и антонимы) - game to learn new words/testing to know level of English\nGood luck!", reply_markup=markup)
                elif language == 'ru':
                    bot.send_message(message.chat.id, text="1)Основная команда - '/menu'. Используется для выбора или смены функции бота. \n2)Если хотите сменить язык, то используйте команду '/language'.\n3)Вы можете скопировать любое слово после перевода, просто нажав на него левой кнопкой мыши.\n4)Функции:\n-Word of the day (Слово дня) - каждый день выводит новое слово\n-Translate words (Перевод слов) - поиск значения слова, а также синонимов и антонимов к нему\n-Game Synonyms and Antonyms (Игра синонимы и антонимы) - режим, запускающий игру по изучению слов/запуск тестирования на определение уровня языка\nЖелаем вам удачи в использовании бота!", reply_markup=markup)

            @bot.message_handler(commands=['menu'])
            def menu(message):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                btn1 = types.KeyboardButton("Word of the day (Слово дня)")
                btn2 = types.KeyboardButton("Translate words (Перевод слов)")
                btn3 = types.KeyboardButton("Game Synonyms and Antonyms (Игра синонимы и антонимы)")
                markup.add(btn1, btn2, btn3)
                if language == 'eng':
                    bot.send_message(message.chat.id, text="Choose the function: ", reply_markup=markup)
                elif language == 'ru':
                    bot.send_message(message.chat.id, text="Выберите функцию: ", reply_markup=markup)

            @bot.message_handler(commands=['A1'])
            def words_A1(message):
                global page_number
                page_number = 1
                A1()
                location = random.randint(1, 4)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn_syn = types.KeyboardButton(game_synonym)
                btn_ant1 = types.KeyboardButton(game_antonyms_1)
                btn_ant2 = types.KeyboardButton(game_antonyms_2)
                btn_ant3 = types.KeyboardButton(game_antonyms_3)
                back = types.KeyboardButton('/menu')
                if location == 1:
                    markup.add(btn_syn, btn_ant1, btn_ant2, btn_ant3, back)
                elif location == 2:
                    markup.add(btn_ant1, btn_syn, btn_ant2, btn_ant3, back)
                elif location == 3:
                    markup.add(btn_ant1, btn_ant2, btn_syn, btn_ant3, back)
                elif location == 4:
                    markup.add(btn_ant1, btn_ant3, btn_ant2, btn_syn, back)
                user_choice = bot.send_message(message.chat.id, f'<code>{word_A1}</code>', parse_mode="HTML", reply_markup=markup)
                bot.register_next_step_handler(user_choice, right_answer)

            @bot.message_handler(commands=['A2'])
            def words_A2(message):
                global page_number
                page_number = 2
                A2()
                location = random.randint(1, 4)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn_syn = types.KeyboardButton(game_synonym)
                btn_ant1 = types.KeyboardButton(game_antonyms_1)
                btn_ant2 = types.KeyboardButton(game_antonyms_2)
                btn_ant3 = types.KeyboardButton(game_antonyms_3)
                back = types.KeyboardButton('/menu')
                if location == 1:
                    markup.add(btn_syn, btn_ant1, btn_ant2, btn_ant3, back)
                elif location == 2:
                    markup.add(btn_ant1, btn_syn, btn_ant2, btn_ant3, back)
                elif location == 3:
                    markup.add(btn_ant1, btn_ant2, btn_syn, btn_ant3, back)
                elif location == 4:
                    markup.add(btn_ant1, btn_ant3, btn_ant2, btn_syn, back)
                user_choice = bot.send_message(message.chat.id, f'<code>{word_A2}</code>', parse_mode="HTML", reply_markup=markup)
                bot.register_next_step_handler(user_choice, right_answer)

            @bot.message_handler(commands=['B1'])
            def words_B1(message):
                global page_number
                page_number = 3
                B1()
                location = random.randint(1, 4)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn_syn = types.KeyboardButton(game_synonym)
                btn_ant1 = types.KeyboardButton(game_antonyms_1)
                btn_ant2 = types.KeyboardButton(game_antonyms_2)
                btn_ant3 = types.KeyboardButton(game_antonyms_3)
                back = types.KeyboardButton('/menu')
                if location == 1:
                    markup.add(btn_syn, btn_ant1, btn_ant2, btn_ant3, back)
                elif location == 2:
                    markup.add(btn_ant1, btn_syn, btn_ant2, btn_ant3, back)
                elif location == 3:
                    markup.add(btn_ant1, btn_ant2, btn_syn, btn_ant3, back)
                elif location == 4:
                    markup.add(btn_ant1, btn_ant3, btn_ant2, btn_syn, back)
                user_choice = bot.send_message(message.chat.id, f'<code>{word_B1}</code>', parse_mode="HTML", reply_markup=markup)
                bot.register_next_step_handler(user_choice, right_answer)

            @bot.message_handler(commands=['B2'])
            def words_B2(message):
                global page_number
                page_number = 4
                B2()
                location = random.randint(1, 4)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn_syn = types.KeyboardButton(game_synonym)
                btn_ant1 = types.KeyboardButton(game_antonyms_1)
                btn_ant2 = types.KeyboardButton(game_antonyms_2)
                btn_ant3 = types.KeyboardButton(game_antonyms_3)
                back = types.KeyboardButton('/menu')
                if location == 1:
                    markup.add(btn_syn, btn_ant1, btn_ant2, btn_ant3, back)
                elif location == 2:
                    markup.add(btn_ant1, btn_syn, btn_ant2, btn_ant3, back)
                elif location == 3:
                    markup.add(btn_ant1, btn_ant2, btn_syn, btn_ant3, back)
                elif location == 4:
                    markup.add(btn_ant1, btn_ant3, btn_ant2, btn_syn, back)
                user_choice = bot.send_message(message.chat.id, f'<code>{word_B2}</code>', parse_mode="HTML", reply_markup=markup)
                bot.register_next_step_handler(user_choice, right_answer)

            @bot.message_handler(commands=['C1'])
            def words_C1(message):
                global page_number
                page_number = 5
                C1()
                location = random.randint(1, 4)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn_syn = types.KeyboardButton(game_synonym)
                btn_ant1 = types.KeyboardButton(game_antonyms_1)
                btn_ant2 = types.KeyboardButton(game_antonyms_2)
                btn_ant3 = types.KeyboardButton(game_antonyms_3)
                back = types.KeyboardButton('/menu')
                if location == 1:
                    markup.add(btn_syn, btn_ant1, btn_ant2, btn_ant3, back)
                elif location == 2:
                    markup.add(btn_ant1, btn_syn, btn_ant2, btn_ant3, back)
                elif location == 3:
                    markup.add(btn_ant1, btn_ant2, btn_syn, btn_ant3, back)
                elif location == 4:
                    markup.add(btn_ant1, btn_ant3, btn_ant2, btn_syn, back)
                user_choice = bot.send_message(message.chat.id, f'<code>{word_C1}</code>', parse_mode="HTML", reply_markup=markup)
                bot.register_next_step_handler(user_choice, right_answer)

            @bot.message_handler(commands=['C2'])
            def words_C2(message):
                global page_number
                page_number = 6
                C2()
                location = random.randint(1, 4)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn_syn = types.KeyboardButton(game_synonym)
                btn_ant1 = types.KeyboardButton(game_antonyms_1)
                btn_ant2 = types.KeyboardButton(game_antonyms_2)
                btn_ant3 = types.KeyboardButton(game_antonyms_3)
                back = types.KeyboardButton('/menu')
                if location == 1:
                    markup.add(btn_syn, btn_ant1, btn_ant2, btn_ant3, back)
                elif location == 2:
                    markup.add(btn_ant1, btn_syn, btn_ant2, btn_ant3, back)
                elif location == 3:
                    markup.add(btn_ant1, btn_ant2, btn_syn, btn_ant3, back)
                elif location == 4:
                    markup.add(btn_ant1, btn_ant3, btn_ant2, btn_syn, back)
                user_choice = bot.send_message(message.chat.id, f'<code>{word_C2}</code>', parse_mode="HTML", reply_markup=markup)
                bot.register_next_step_handler(user_choice, right_answer)

            @bot.message_handler(commands=['I_do_not_know'])
            def no_level(message):
                global level
                if language == 'ru':
                    bot.send_message(message.chat.id, text='Предлагаем вам пройти тест!')
                    bot.send_message(message.chat.id, "Если захотите прекратить тестирование, то введите '/menu'")
                elif language == 'eng':
                    bot.send_message(message.chat.id, text="Let's start from the test!")
                    bot.send_message(message.chat.id, "If you want to stop the test, then enter '/menu'")
                global score
                score = 0
                global trying_5
                trying_5 = 0
                global mistakes
                mistakes = 0
                global res
                res = str()
                global level
                level = 'A1'
                testing(message)

            @bot.message_handler(content_types=['text'])
            def func(message):
                if (message.text == "Word of the day (Слово дня)"):
                    parser(URL_1)
                    print(word_of_the_day)
                    bot.send_message(message.chat.id, f'<code>{word_of_the_day}</code>' + " - " + word_definition_day, parse_mode="HTML")
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    menu = types.KeyboardButton("/menu")
                    markup.add(menu)
                    if language == 'eng':
                        bot.send_message(message.chat.id, text='Go to the menu?', reply_markup=markup)
                    elif language == 'ru':
                        bot.send_message(message.chat.id, text='Перейти в меню?', reply_markup=markup)
                    return
                elif (message.text == "Translate words (Перевод слов)"):
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    menu = types.KeyboardButton("/menu")
                    markup.add(menu)
                    if language == 'eng':
                        bot.send_message(message.chat.id, text="If you want to stop, enter '/menu'")
                        msg = bot.send_message(message.chat.id, text='Enter word:', reply_markup=markup)
                    elif language == 'ru':
                        bot.send_message(message.chat.id, text="Если хотите закончить перевод, то введите '/menu'")
                        msg = bot.send_message(message.chat.id, text='Введите слово:', reply_markup=markup)
                    bot.register_next_step_handler(msg, translation)
                elif (message.text == 'Game Synonyms and Antonyms (Игра синонимы и антонимы)'):
                    if language == 'eng':
                        bot.send_message(message.chat.id, text='If you know, choose your level of English')
                    elif language == 'ru':
                        bot.send_message(message.chat.id, text='Если вы знаете свой уровень языка, то выберите его.')
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn1 = types.KeyboardButton("/A1")
                    btn2 = types.KeyboardButton("/A2")
                    btn3 = types.KeyboardButton("/B1")
                    btn4 = types.KeyboardButton("/B2")
                    btn5 = types.KeyboardButton("/C1")
                    btn6 = types.KeyboardButton("/C2")
                    btn7 = types.KeyboardButton("/I_do_not_know (Я не знаю)")
                    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
                    if language == 'eng':
                        bot.send_message(message.chat.id, text="Enter '/menu', if you want to stop game and go to the menu", reply_markup=markup)
                        bot.send_message(message.chat.id, text="Rules: Bot sends word and makes 4 buttons (1 synonym and 3 antonyms), you need to choose button with synonym.", reply_markup=markup)
                    elif language == 'ru':
                        bot.send_message(message.chat.id, text="Введите '/menu', если хотите прекратить игру и вернуться в меню.", reply_markup=markup)
                        bot.send_message(message.chat.id, text="Правила: Бот отправляет слово, а также создает 4 кнопки (1 кнопка с синонимом и 3 кнопки с антонимами). Вам требуется выбрать кнопку с синонимом.", reply_markup=markup)
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn1 = types.KeyboardButton("/menu")
                    markup.add(btn1)
                    if language == 'eng':
                        bot.send_message(message.chat.id, text='Error', reply_markup=markup)
                    elif language == 'ru':
                        bot.send_message(message.chat.id, text="Ошибка", reply_markup=markup)
            bot.polling(none_stop=True)
        except: continue

while True:
    programm()


