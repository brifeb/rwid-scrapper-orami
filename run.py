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
    price = soup.find('h4', attrs={'class':'card-price'}).text.strip()
    stock = soup.find('span', attrs={'class':'card-stock'}).text.strip().replace('stock: ','')
    category = soup.find('span', attrs={'class': 'card-category'}).text.strip().replace('category: ', '')
    description = soup.find('p', attrs={'class': 'card-text'}).text.strip().replace('Description: ', '')


    dict_data = {
        'title' : title,
        'price' : price,
        'stock' : stock,
        'category' : category,
        'description' : description
    }

    print(dict_data)

    with open(f"./result{url_detail}.json", "w") as outfile:
        json.dump(dict_data,outfile)


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
    for url in all_url:
        get_detail(url)

    create_csv()


if __name__ == '__main__':
    run()