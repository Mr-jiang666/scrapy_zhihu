import os
import re

from zhihu_project.zhihu_cookie import zh_selenium


def get_cookie():
    if os.path.exists("zh_cookie.txt"):
        with open("zh_cookie.txt", "r") as f:
            try:
                cookie = f.readlines(1)[0]
            except:
                zh_selenium.run()
                cookie = f.readlines(1)[0]
        r = re.compile(r"'(.*?)': '(.*?)'")
        result = r.findall(cookie)
        cookie_dict = {}
        for item in result:
            cookie_dict[item[0]] = item[1]
        return cookie_dict
    else:
        zh_selenium.run()
        get_cookie()


if __name__ == '__main__':
    cookie = get_cookie()
    print(cookie)