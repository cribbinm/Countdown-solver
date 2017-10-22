import requests, bs4
import sqlite3
import inflect
p = inflect.engine()


def url_creator(letters,page):
    if page == 1:
        return 'https://www.bestwordlist.com/{}letterwords.htm'.format(letters)
    return 'https://www.bestwordlist.com/{}letterwordspage{}.htm'.format(letters, page)


def last_page(letters):
    url = 'https://www.bestwordlist.com/{}letterwords.htm'.format(letters)
    res = requests.get(url)
    res.raise_for_status()
    elements = bs4.BeautifulSoup(res.text,'html.parser')
    last = elements.select('p a.f2')[-1].getText()
    return last

def word_scraper(letters):
    print('Downloading all ' + letters + ' letter words')
    number_of_pages = eval(last_page(letters))
    total = []
    for i in range(1,number_of_pages+1):
        url = url_creator(letters,i)
        res = requests.get(url)
        res.raise_for_status()
        elements = bs4.BeautifulSoup(res.text,'html.parser')
        data = elements.select('p span.mot') + elements.select('p span.mot2')
        words = [item for entry in data for item in entry.getText().strip().split(' ')]
        total += words
    data_entry(letters, total)
    # return total


conn = sqlite3.connect('test.db')
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()
c.execute('Create TABLE if not exists server(nine REAL, eight REAL, seven REAL, six REAL, five REAL, four REAL)')

def data_entry(letters, ls):
    for item in ls:
        c.execute("INSERT INTO server(" + p.number_to_words(letters) + ") VALUES(?)", (item,))
    conn.commit()


def query_data(letters):
    c.execute("SELECT " + p.number_to_words(letters) + " FROM server")
    ls = c.fetchall()
    return list(filter(None.__ne__, ls))


word_scraper(9)
word_scraper(8)
word_scraper(7)
word_scraper(6)
word_scraper(5)
word_scraper(4)

conn.close()