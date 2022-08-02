import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, url):
    api_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {'Authorization': f'Bearer {token}'}
    body = {"long_url": url}
    response = requests.post(api_url, json=body, headers=headers)
    response.raise_for_status()
    return response.json()['link']


def get_clicks(token, bitlink):
    url = urlparse(bitlink)
    short_bitlink = f'{url.netloc}{url.path}'
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{short_bitlink}/clicks/summary'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(TOKEN, url):
    if 'bit.ly' in url:
        try:
            count_clicks = get_clicks(TOKEN, url)
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
    BITLY_TOKEN = os.getenv('token')
    url = input('Введите ссылку:').strip()
    print(is_bitlink(BITLY_TOKEN, url))


if __name__ == '__main__':
    main()
