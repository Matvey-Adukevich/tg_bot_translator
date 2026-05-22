from gtts import gTTS
import requests
from bs4 import BeautifulSoup as b
# def parser_audio(wordtofind):
#     s = gTTS(wordtofind)
#     s.save(f'.//audio//{wordtofind}_audio.mp3')
def parser():
    r = requests.get('https://www.dictionary.com/e/word-of-the-day/')
    soup = b(r.text, 'html.parser')
    word_of_the_day_1 = soup.find_all('h1', class_='js-fit-text')
    x = [c.text for c in word_of_the_day_1]
    global word_of_the_day
    word_of_the_day = str(x[0])
    URL_2 = 'https://www.dictionary.com/browse/'
    m = requests.get(URL_2 + word_of_the_day)
    soup = b(m.text, 'html.parser')
    word_day_def = soup.find_all('div', class_='NZKOFkdkcvYgD3lqOIJw')
    definition_word_day = [c.text for c in word_day_def]
    global word_definition_day
    word_definition_day = str(definition_word_day[0])
    print(word_of_the_day,word_definition_day)
parser()
