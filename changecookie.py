import yaml
import random


class ChangeCookie:
    def __init__(self):

        self.cookies_sum = 0
        self.cookie_count = 0

        try:
            with open('cookies.yaml', 'r') as file:
                self.config = yaml.safe_load(file)
        except Exception as e:
            print(f"读取文件时发生未知错误：{e}")

        # 访问 cookies 列表
        self.cookies = self.config['cookies']
        self.cookies_sum = len(self.cookies)

        # 获取User-Agent
        self.user_agent = self.config['user_agent']

    def get_user_agent(self):
        return random.choice(self.user_agent)

    def get_cookie(self):
        print(f"当前cookie: {self.cookie_count} / {self.cookies_sum}")
        if self.cookie_count < self.cookies_sum:
            sso = self.cookies[self.cookie_count]
            self.cookie_count += 1
            return sso
        else:
            self.cookie_count = 0
            return self.cookies[self.cookie_count]


if __name__ == '__main__':
    test = ChangeCookie()
    print(test.get_user_agent())
    print(test.get_user_agent())
