import requests
import os
from dotenv import load_dotenv

TOKEN = os.getenv('token')


def shorten_link(token, url):
    api_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {'Authorization': f'Bearer {token}'}
    body = {"long_url": f"{url}"}
    response = requests.post(api_url, json=body, headers=headers)
    response.raise_for_status()
    return response.json()['link']


def total_clicks(token, bitlink):
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(TOKEN, url):
    if 'bit.ly' in url:
        try:
            t = total_clicks(TOKEN, url)
            print(f'По вашей ссылке прошли {t} раз(а)')
            # print(f'По вашей ссылке прошли {t["total_clicks"]} раз(а)')
        except requests.exceptions.HTTPError as error:
            exit("Can't get data from server:\n{0}".format(error))
    else:
        try:
            bitlink = shorten_link(TOKEN, url)
            print('Битлинк', bitlink)
        except requests.exceptions.MissingSchema:
            print('Вы ввели неправильный URL')
        except requests.exceptions.HTTPError as error:
            exit("Can't get data from server:\n{0}".format(error))


def main():
    load_dotenv()
    TOKEN = os.getenv('token')
    print('Введите ссылку:')
    url = input()
    is_bitlink(TOKEN, url)


if __name__ == '__main__':
    main()
