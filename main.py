import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

TOKEN = os.getenv('token')
#       https://bit.ly/3JkG0mU

def shorten_link(token, url):
    api_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {'Authorization': f'Bearer {token}'}
    body = {"long_url": f"{url}"}
    response = requests.post(api_url, json=body, headers=headers)
    response.raise_for_status()
    return response.json()['link']


def total_clicks(token, bitlink):
    url = urlparse(bitlink)
    short_bitlink = url.netloc + url.path
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{short_bitlink}/clicks/summary'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(TOKEN, url):
    if 'bit.ly' in url:
        try:
            count_clicks = total_clicks(TOKEN, url)
        except requests.exceptions.HTTPError as error:
            exit("Can't get data from server:\n{0}".format(error))
        return f'По вашей ссылке прошли {count_clicks} раз(а)'
    else:
        try:
            bitlink = shorten_link(TOKEN, url)
        except requests.exceptions.MissingSchema:
            return 'Вы ввели неправильный URL'
        except requests.exceptions.HTTPError as error:
            exit("Can't get data from server:\n{0}".format(error))
        return f'Битлинк {bitlink}'

def main():
    load_dotenv()
    TOKEN = os.getenv('token')
    # print('Введите ссылку:''Введите ссылку:')
    url = input('Введите ссылку:').strip()
    print(is_bitlink(TOKEN, url))


if __name__ == '__main__':
    main()
