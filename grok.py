import json
import httpx
import requests

from changecookie import ChangeCookie


class GrokRequest:
    grok_url: str = "https://grok.com/rest/app-chat/conversations/new"

    headers = {
        "authority": "grok.com",
        "accept": "*/*",
        "content-type": "application/json",
        "cookie": "",
        "origin": "https://grok.com",
        "referer": "https://grok.com/?referrer=website",
        "user-agent": ""

    }

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(240))
        self.change_cookie = ChangeCookie()
        self.set_cookie(self.change_cookie.get_cookie())
        self.set_user_agent(self.change_cookie.get_user_agent())
        print(self.headers)

    def set_cookie(self, cookie: str):
        self.headers["cookie"] = cookie

    def set_user_agent(self, agent: str):
        self.headers["user-agent"] = agent

    async def get_grok_request(self, message, model):
        data = {"message": message, "modelName": model}
        try:
            async with self.client.stream("POST", self.grok_url, headers=self.headers, json=data) as response:
                if response.status_code == 200:
                    print("200 Okay!")
                    async for line in response.aiter_lines():
                        if line:  # 过滤掉空行
                            try:
                                # 解析 JSON 格式
                                data = json.loads(line)
                                # 提取 token
                                token = data.get("result", {}).get("response", {}).get("token")
                                if token:
                                    # print(token, end="", flush=True)  # 逐字输出
                                    # self.tokens.append(token)
                                    yield token
                            except json.JSONDecodeError:
                                print("\nJSON error:", line)
                    print("\n流式结束！")
                else:
                    try:
                        error_message = await response.aread()
                        self.set_cookie(self.change_cookie.get_cookie())
                        self.set_user_agent(self.change_cookie.get_user_agent())
                        print(self.headers)
                        print("Error:", response.status_code, error_message)
                        yield str(response.json())
                    except json.JSONDecodeError:
                        print("Error:", response.text)

        except requests.exceptions.Timeout:
            print("\n Time out!")

        except requests.exceptions.RequestException as e:
            print("\nError:", str(e))

