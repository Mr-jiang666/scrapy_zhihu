# -*- coding: utf-8 -*-
import re
import time
import json
import requests
import base64
from io import BytesIO
from sys import version_info
from mouse import move, click
from selenium import webdriver
from PIL import Image
from zhihu_project.zheye import zheye
from selenium.webdriver.chrome.options import Options

class ZhihuSpider():
    def __init__(self):
        self.url = "https://www.zhihu.com/"
        chrome_option = Options()
        chrome_option.add_argument("--disable-extensions")
        chrome_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.browser = webdriver.Chrome(options=chrome_option)

    def img_text(self,uname, pwd,  img):
        img = img.convert('RGB')
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        if version_info.major >= 3:
            b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
        else:
            b64 = str(base64.b64encode(buffered.getvalue()))
        data = {"username": uname, "password": pwd,"typeid": "16","image": b64}
        result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            return result["message"]

    def yanzhengma(self,yzm_user,yzm_psw):
        #截图验证码图片
        #定位某个元素在浏览器中的位置
        time.sleep(2)
        try:
            english_captcha_element = self.browser.find_element_by_class_name("Captcha-englishImg")
        except:
            english_captcha_element = None
        try:
            chinese_captcha_element = self.browser.find_element_by_class_name("Captcha-chineseImg")
        except:
            chinese_captcha_element = None
        if english_captcha_element:
            image_file_name = "yzm_en.png"
            location = english_captcha_element.location
            size = english_captcha_element.size
            top, buttom, left, right = location["y"], location["y"] + size["height"], location["x"], location['x'] + size["width"]
            screenshot = self.browser.get_screenshot_as_png()
            screenshot = Image.open(BytesIO(screenshot))
            captcha = screenshot.crop((int(left), int(top), int(right), int(buttom)))
            captcha.save(image_file_name)
            img = Image.open(image_file_name)
            result = self.img_text(uname=yzm_user, pwd=yzm_psw, img=img)
            print(result)
            time.sleep(2)
            try:
                text_ele = self.browser.find_element_by_xpath("//label[@class='Input-wrapper']//input[@class='Input']")
            except:
                text_ele = None
            if text_ele:
                text_ele.send_keys(result)
                time.sleep(2)
            else:
                self.yanzhengma()
        elif chinese_captcha_element:
            ele_postion = chinese_captcha_element.location
            x_relative = ele_postion["x"]
            y_relative = ele_postion["y"]
            browser_navigation_panel_height = self.browser.execute_script('return window.outerHeight - window.innerHeight;')
            base64_text = chinese_captcha_element.get_attribute("src")
            code = base64_text.replace("data:image/jpg;base64,", "").replace("%0A", "")
            fh = open("yzm_cn.jpeg", "wb")
            fh.write(base64.b64decode(code))
            fh.close()
            z = zheye()
            positions = z.Recognize('yzm_cn.jpeg')
            last_position = []
            if len(positions) == 2:
                if positions[0][1] > positions[1][1]:
                    last_position.append([positions[1][1], positions[1][0]])
                    last_position.append([positions[0][1], positions[0][0]])
                else:
                    last_position.append([positions[0][1], positions[0][0]])
                    last_position.append([positions[1][1], positions[1][0]])
                first_position = [int(last_position[0][0] / 2), int(last_position[0][1] / 2)]
                second_position = [int(last_position[1][0] / 2), int(last_position[1][1] / 2)]
                move(x_relative + first_position[0], y_relative + browser_navigation_panel_height + first_position[1])
                click()
                time.sleep(3)
                move(x_relative + second_position[0],
                     y_relative + browser_navigation_panel_height + second_position[1])
                click()
            else:
                last_position.append([positions[0][1], positions[0][0]])
                first_position = [int(last_position[0][0] / 2), int(last_position[0][1] / 2)]
                move(x_relative + first_position[0],y_relative + browser_navigation_panel_height + first_position[1])
                click()

    def login(self):
        zh_username = input("请输入知乎账号：")
        zh_password = input("请输入知乎密码：")
        yzm_user = input("请输入图鉴网账号：")
        yzm_psw = input("请输入图鉴网密码：")
        self.browser.find_element_by_xpath("//div[@class='SignFlow-tab']").click()
        username_ele = self.browser.find_element_by_xpath("//div[@class='SignFlow-account']//input[@class='Input']")
        password_ele = self.browser.find_element_by_xpath("//div[@class='SignFlow-password']//input[@class='Input']")
        username_ele.send_keys(zh_username)
        password_ele.send_keys(zh_password)
        while True:
            self.browser.find_element_by_xpath("//button[@class='Button SignFlow-submitButton Button--primary Button--blue']").click()
            time.sleep(2)
            try:
                notify_ele = self.browser.find_element_by_class_name("TopstoryTabs-link Topstory-tabsLink")
            except:
                notify_ele = None
            if notify_ele:
                return self.browser.page_source
            else:
                self.yanzhengma(yzm_user,yzm_psw)

    def run(self):
        try:
            self.browser.maximize_window()  # 很重要！！
        except:
            pass
        self.browser.get(self.url)
        time.sleep(3)
        if '等你来答' in self.browser.page_source:
            page_source = self.browser.page_source
        else:
            page_source = self.login()
        search_text = re.compile(r'</script><script id="js-initialData" type="text/json">(.*?)</script>')
        search_result = search_text.search(page_source).group(1)
        data = json.loads(search_result)
        next_url = data['initialState']['topstory']['recommend']['serverPayloadOrigin']['paging']['next']
        self.browser.get(next_url)
        Cookies = self.browser.get_cookies()
        cookie_dict = {}
        for cookie in Cookies:
            # 写入文件
            f = open('zh_cookie.txt', 'w', encoding='utf-8')
            cookie_dict[cookie['name']] = cookie['value']
            f.write(str(cookie_dict))
            f.close()
        return next_url


zh_selenium = ZhihuSpider()


# if __name__ == '__main__':
#     zh_selenium.run()
