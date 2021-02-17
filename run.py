import requests, json
from bs4 import BeautifulSoup

session = requests.Session()

def login():
    print('login...')
    datas = {
        'username': 'user',
        'password': 'user12345'
    }
    res = session.post('http://0.0.0.0:5000/login', data=datas)

    soup = BeautifulSoup(res.text, features="html.parser")

    page_item = soup.find_all('li', attrs=('class','page-item'))

    total_pages = len(page_item) - 2

    return total_pages


def get_urls(page):
    print('get urls ...  page {}'.format(page))

    params = {
        'page': page
    }

    res = session.get('http://0.0.0.0:5000/', params = params)

    soup = BeautifulSoup(res.text, "html.parser")
    # soup = BeautifulSoup(open('res.html'), "html.parser")
    titles = soup.find_all('h4', attrs={'class': 'card-title'})

    urls = []

    for title in titles:
        url = title.find('a')['href']
        urls.append(url)

    return urls

    # print(urls)


def get_detail(url_detail):
    print('get details..')

    url = "http://0.0.0.0:5000" + url_detail
    print(url)

    res = session.get(url)

    # f = open('./res.html', 'w+')
    # f.write(res.text)
    # f.close()

    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.find('title').text.strip()
    print(title)




def create_csv():
    print('csv generated..')


def run():
    total_pages = login()

    # total_urls = []
    # for i in range(total_pages):
    #     page = i +1
    #     urls = get_urls(page)
    #     total_urls += urls
    # with open('all_urls.json', 'w') as outfile:
    #     json.dump(total_urls, outfile)

    with open('all_urls.json') as json_file:
        all_url = json.load(json_file)

    print(all_url[0])

    get_detail(all_url[0])
    create_csv()


if __name__ == '__main__':
    run()