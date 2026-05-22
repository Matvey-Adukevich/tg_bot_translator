from requests_html import HTMLSession
from bs4 import BeautifulSoup as b

session13 = HTMLSession()
word = ' sea'

klg = f'https://dictionary.cambridge.org/ru/thesaurus/{word}'
klg = ''.join(klg.split())
m = session13.get(klg)
soup_2 = b(m.text, 'html.parser')
synonyms_1 = soup_2.find_all(class_='dx-h dthesButton synonym')
w = list(set(nh.text for nh in synonyms_1))
print(198)
print(w)