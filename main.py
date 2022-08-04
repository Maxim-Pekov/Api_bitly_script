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
    return bitlink


def get_clicks(token, bitlink):
    url = urlparse(bitlink)
    short_bitlink = f'{url.netloc}{url.path}'
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{short_bitlink}/clicks/summary'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    count_clicks = response.json()['total_clicks']
    return count_clicks


def is_bitlink(token, bitlink):
    url = urlparse(bitlink)
    short_bitlink = f'{url.netloc}{url.path}'
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{short_bitlink}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(api_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    url = input('Введите ссылку:').strip()
    try:
        if is_bitlink(token, url):
            print(f'По вашей ссылке прошли {get_clicks(token, url)} раз(а)')
        else:
            print(f'Битлинк: {shorten_link(token, url)}')
    except requests.exceptions.HTTPError as error:
        print(f"Can't get data from server:\n{error}")


if __name__ == '__main__':
    main()
