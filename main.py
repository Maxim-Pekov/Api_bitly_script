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
    bitlink = response.json()['link']
    return f'Битлинк: {bitlink}'


def get_clicks(token, bitlink):
    url = urlparse(bitlink)
    short_bitlink = f'{url.netloc}{url.path}'
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{short_bitlink}/clicks/summary'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    count_clicks = response.json()['total_clicks']
    return f'По вашей ссылке прошли {count_clicks} раз(а)'


def is_bitlink(token, bitlink):
    url = urlparse(bitlink)
    short_bitlink = f'{url.netloc}{url.path}'
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{short_bitlink}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 404:
        return False
    response.raise_for_status()
    return True


def choice_link(token, url):
    if is_bitlink(token, url):
        return get_clicks(token, url)
    return shorten_link(token, url)


def main():
    load_dotenv()
    BITLY_TOKEN = os.getenv('token')
    url = input('Введите ссылку:').strip()
    try:
        link = choice_link(BITLY_TOKEN, url)
    except requests.exceptions.HTTPError as error:
        print(f"Can't get data from server:\n{error}")
    print(link)


if __name__ == '__main__':
    main()
