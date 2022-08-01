import requests

token = 'c6d39b44191b42c930dcacd0e008ec335fbb0f20'


# url = 'https://api-ssl.bitly.com/v4/bitlinks'

def shorten_link(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    body = {"long_url": "https://github.com/maxim-pekov"}
    response2 = requests.post(url, json=body, headers=headers)
    return response2.json()['link']


def main():
    print('Введите ссылку которую хотите уменьшить:')
    url = input()
    # bitlink = ''
    try:
        bitlink = shorten_link(token, url)
        print('Битлинк', bitlink)

    except requests.exceptions.MissingSchema:
        print('Вы ввели неправильный URL')
    except requests.exceptions.HTTPError as error:
        exit("Can't get data from server:\n{0}".format(error))


# shorten_link(token, url)
# url2 = 'https://api-ssl.bitly.com/v4/user'
#
# headers = {
#     'Authorization': 'Bearer c6d39b44191b42c930dcacd0e008ec335fbb0f20'
# }
# response = requests.get(url, headers=headers)
# response.raise_for_status()


if __name__ == '__main__':
    main()
