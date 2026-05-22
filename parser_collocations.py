from bs4 import BeautifulSoup
# from requests_html import HTMLSession


def parser_collocations(wordtofind, c):
    try:
        # print(wordtofind)
        # wordtofind = wordtofind.lower()
        # for i in wordtofind:
        #     if i not in 'qwertyuiopasdfghjklzxcvbnm':
        #         return ''
        #         # break
        # print(wordtofind)
        # session = HTMLSession()
        # wordtofind = 'winter'
        # c = session.get(f'https://www.linguatools.de/kollokationen-en/bolls/?utf8=%E2%9C%93&lemmahits=100&query={wordtofind}&commit=Search+Collocations%21')
        soup3 = BeautifulSoup(c.text, 'html.parser')
        word2 = soup3.find_all(class_='table table-striped table-bordered table-hover table-condensed')
        gf = [d.text for d in word2]

        for i in gf:
            a = i

        b = []
        a = a.replace(wordtofind, '*')
        a = a.split('\n')

        for i in a:
            if i != '':
                b.append(i)

        c = []

        for i in b:
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

        rt = [] #collocations

        for i in yt:
            rt.append(i[1])

        return rt
    except:
        return ''

