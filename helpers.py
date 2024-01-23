import jinja2
from http.cookies import BaseCookie


template_environment = jinja2.Environment()

cookies_handler = BaseCookie()


def get_cookies_dict(raw_cookies:str)->dict:
    cookies = {}
    cookies_handler.load(rawdata=raw_cookies)
    for key, morsel in cookies_handler.items():
        cookies[key] = morsel.value
    cookies_handler.clear()
    return cookies


def template(template_name:str,context:dict={}):
    with open('templates/'+template_name,"r") as template_file:
        text_html = template_file.read()
    text_html = template_environment.from_string(text_html).render(context)
    return text_html