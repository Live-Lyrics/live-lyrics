import os

import vk_api

proxies = {
    'http':  'http://66.70.191.215:1080',
    'https': 'http://66.70.191.215:1080'
}


def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


def vk_sign_in():
    login, password = os.environ.get('VK_LOGIN'), os.environ.get('VK_PASSWORD')
    vk_session = vk_api.VkApi(login, password, captcha_handler=captcha_handler)
    vk_session.http.proxies = proxies

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    return vk
