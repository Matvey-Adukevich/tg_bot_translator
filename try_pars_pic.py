from requests_html import HTMLSession
from bs4 import BeautifulSoup as b
from PIL import Image

session1 = HTMLSession()
word = input('input: ')
response = session1.get(f'https://ru.freepik.com/search?format=search&query={word}&type=photo')
soup = b(response.text, features="html.parser")
images = []
for img in soup.findAll('img'):
    images.append(img.get('src'))
images = images[10]

session2 = HTMLSession()
p = session2.get(images).content

out = open(f".//pictures//{word}.png", "wb")
out.write(p)
out.close()
# p.save(f'{word}', 'png', quality=100)
# img_data = session2.get(url).content
# with open('image.jpg', 'wb') as f:
#    f.write(img_data)

