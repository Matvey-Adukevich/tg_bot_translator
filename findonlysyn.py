from requests_html import HTMLSession
from gensim.models import Word2Vec

session18 = HTMLSession()

def f(m):
    word = Word2Vec.load('wv')
    a = ''
    word10 = word.wv.most_similar(m.lower(), topn=1)
    a = word10[0][0]
    print(3)
    return a

def only_synonym(message):
    k = ''
    print(message.lower())
    r = session18.head(f'https://www.dictionary.com/browse/{message.lower()}')
    status = int(r.status_code)
    print(status)
    if status == 200:
        k = f(message.lower())
        if k!='':
            print(k)
    elif status != 200 or k == '':
        print(4)
        only_synonym(input(2))

print(only_synonym(str(input(1))))


                # soup_1 = b(r.text, 'html.parser')
                # translation_1 = soup_1.find_all('div', class_='ESah86zaufmd2_YPdZtq')
                # a = [c.text for c in translation_1]
                # if a == []:
                #     if language == 'eng':
                #         bot.send_message(message.chat.id, "Sorry, we can't find this word/collocation. Check your word and try again.")
                #     elif language == 'ru':
                #         bot.send_message(message.chat.id, text="Извините, мы не можем найти это слово/словосочетание. Проверьте его написание и попробуйте снова.")
                #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                #     btn1 = types.KeyboardButton("/menu")
                #     markup.add(btn1)
                #     if language == 'eng':
                #         msg2 = bot.send_message(message.chat.id, text='Enter word:', reply_markup=markup)
                #     elif language == 'ru':
                #         msg2 = bot.send_message(message.chat.id, text='Введите слово:', reply_markup=markup)
                #     bot.register_next_step_handler(msg2, translation)
                # if a!=[]:
                #     translation_threads(message.text)