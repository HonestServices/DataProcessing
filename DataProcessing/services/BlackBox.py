import asyncio
import json
from contextlib import suppress
from typing import Optional

from aiohttp import ClientSession
from playwright._impl._errors import TargetClosedError
from playwright.async_api import Request, Response, async_playwright
from redis.asyncio import Redis
from tools import timeit

from .Base import BaseService, cache

try:
    from asyncio import timeout
except ImportError:
    try:
        from async_timeout import timeout
    except ImportError:
        from async_timeout import Timeout as timeout


class BlackBoxService(BaseService):
    def __init__(self: "BlackBoxService", redis: Redis, ttl: Optional[int] = None):
        self.redis = redis
        self.ttl = ttl
        super().__init__("BlackBox", self.redis, self.ttl)
        self.session_id = "98a437c6-22eb-4583-af8d-cab6c6842db2"
        self.user_id = "65d93bbc9ba56f00325371f2"

    async def __prompt(self, prompt: str, expert: str = "") -> str:
        prompt = (
            prompt.replace("'", "\u2018")
            .replace("'", "\u2019")
            .replace('"', "\u201c")
            .replace('"', "\u201d")
            .replace("'", "\u0027")
            .replace('"', "\u0022")
        )

        async with ClientSession() as session:
            headers = {
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.6",
                "content-type": "application/json",
                "cookie": f"sessionId={self.session_id}; intercom-device-id-jlmqxicb=67b29805-1ee5-4b56-96b1-005536e9f34a; __Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..aBt7a4Nnsq8QFyPf.v6QbMNGWBnPybTE_NKF1VKJ1RinOwIV_DapDtO4JPSx9GSymMOMI_FxBkf7_A-7GXtTVZ8DGXUWQDrxpFcLi7hCQIdMVaoqoYOOmdHeFNVeIp1R1tRozMaQGMg4bNYcWu3ET2-JmMGdPU9OiYH_dUX15QtAanxKJ7vAB_HlJx00n2eu_HA0YGMdzfl20zJsftiqmowOLMM1T4Z9jmZVyN4CcLqyUFVQZJ5M-_Zhxf7oXWVzD36pVVGewX6cBsZLM4Iw3SHEJCd31b8UX3dS31aRwIrQwoVZbFmUElGrvNi0YjxKF_-v37LPfUoNzSHgDfv3Y9NPST1zbMw0Ao8jq6V_ydmgBkr7qn4h5ZRgROth_TcfVVnBJz7Dv-TZZrpMuV3avlq9F08TkpU7VCsJcApH2PDbXFCaDVGpEZRI7j2-Wup8s5cErJIEliy5CPUa1smzx0hwxSbScnCd-WKwgm20QI2xIP3Unv1tX-1YsjLrTyw.Kuj2uTjjHZdBzpaOKBnaaw; personalId=567aa5e4-a01b-4f3e-b77b-1a175baacb55; intercom-session-jlmqxicb=SkZRZnlkUVBIRm42OUhkdVdFcXJwZjU5M1o5Vk1PbCtZRUtQK3BKVkw2MjJWK0V3T3dsNmVZMzAvSDJ4OE1GVi0tSzZrUTZkaTFaR3A1UXp2QzJpTlZDZz09--6c97bef96363230490ce325ead039a73f27ccea7",
                "origin": "https://www.blackbox.ai",
                "referer": "https://www.blackbox.ai/chat",
                "sec-ch-ua": '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "sec-gpc": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            }

            data = {
                "messages": [{"id": "UddxGeR", "content": prompt, "role": "user"}],
                "previewToken": None,
                "userId": self.user_id,
                "codeModelMode": True,
                "agentMode": {},
                "trendingAgentMode": {"mode": True, "id": expert.lower()},
                "isMicMode": False,
                "isChromeExt": False,
                "githubToken": None,
                "validated": "69783381-2ce4-4dbd-ac78-35e9063feabc",
            }

            async with session.post(
                "https://www.blackbox.ai/api/chat", json=data, headers=headers
            ) as response:
                response_data = await response.text()

                ret = (
                    "\n".join(response_data.splitlines()[2:])
                    if "Sources:" in response_data
                    else response_data
                )

                if "$@$" in ret:
                    ret = ret[ret.index("$@$", 2) + 3 :]

                if "$~~~$" in ret:
                    ret = ret[ret.index("$~~~$", 2) + 5 :]
        ret = ret.replace("<br>", "")
        return ret

    async def _prompt(self, prompt: str, expert: str = "") -> str:
        prompt = (
            prompt.replace("'", "\u2018")
            .replace("'", "\u2019")
            .replace('"', "\u201c")
            .replace('"', "\u201d")
            .replace("'", "\u0027")
            .replace('"', "\u0022")
        )
        async with ClientSession(
            cookies={
                "sessionId": {self.session_id},
                "__Host-authjs.csrf-token": "07ac7d6e2f339f1f95d780460da3f45a2bb5b7de234a5af9aa6ec85878d2481c%7Cfe261e5ae2b8a58337095e0911b5411ece1994c4d7916b9a4b7073d5a7771846",
                "__Secure-authjs.callback-url": "https%3A%2F%2Fwww.blackbox.ai",
            }
        ) as session:

            headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-US,en;q=0.6",
                "cache-control": "no-cache",
                "origin": "https://www.blackbox.ai",
                "pragma": "no-cache",
                "priority": "u=1, i",
                "referer": "https://www.blackbox.ai/",
                "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "sec-gpc": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            }

            # First POST request
            json_1 = {
                "query": prompt,
                "messages": [{"id": "iU1JsxF", "content": prompt, "role": "user"}],
                "index": None,
            }
            async with session.post(
                "https://www.blackbox.ai/api/check", json=json_1, headers=headers
            ) as response_1:
                __ = await response_1.json()  # noqa: F841

            # Second POST request
            json_2 = {
                "messages": [{"id": "iU1JsxF", "content": prompt, "role": "user"}],
                "id": "iU1JsxF",
                "previewToken": None,
                "userId": None,
                "codeModelMode": True,
                "agentMode": {},
                "trendingAgentMode": (
                    {"mode": True, "id": expert.lower()} if expert.lower() != "" else {}
                ),
                "isMicMode": False,
                "userSystemPrompt": None,
                "maxTokens": 1024,
                "playgroundTopP": None,
                "playgroundTemperature": None,
                "isChromeExt": False,
                "githubToken": "",
                "clickedAnswer2": False,
                "clickedAnswer3": False,
                "clickedForceWebSearch": False,
                "visitFromDelta": False,
                "mobileClient": False,
                "userSelectedModel": None,
                "validated": "00f37b34-a166-4efb-bce5-1312d87f2f94",
                "imageGenerationMode": False,
                "webSearchModePrompt": False,
                "deepSearchMode": False,
            }
            async with session.post(
                "https://www.blackbox.ai/api/chat", json=json_2, headers=headers
            ) as response_2:
                response_data = await response_2.text()

        ret = (
            "\n".join(response_data.splitlines()[2:])
            if "Sources:" in response_data
            else response_data
        )

        if "$@$" in ret:
            ret = ret[ret.index("$@$", 2) + 3 :]

        if "$~~~$" in ret:
            ret = ret[ret.index("$~~~$", 2) + 5 :]
        ret = ret.replace("<br>", "")
        ret = (
            ret.replace(", try unlimited chat https://www.blackbox.ai/", "")
            .replace("blackbox.ai", "honest.rocks")
            .replace("blackbox", "honest")
        )
        return ret

    async def browser_prompt(self, prompt: str, expert: str = "") -> str:
        async def execute():
            if not hasattr(self, "cookies"):
                with open("/root/cookies/www.blackbox.ai.cookies.json", "r") as f:
                    self.cookies = json.load(f)
            loop = asyncio.get_running_loop()
            fut = loop.create_future()
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
                )
                await context.add_cookies(self.cookies)
                page = await context.new_page()

                async def cleanup():
                    await page.close()
                    await context.close()
                    await browser.close()

                async def get_payload(r: Request):
                    if r.url == "https://www.blackbox.ai/api/chat":
                        if fut.done():
                            return
                        resp = await r.response()
                        with suppress(asyncio.InvalidStateError):
                            fut.set_result(await resp.text())

                page.on("request", get_payload)
                try:
                    await page.goto(
                        "https://www.blackbox.ai/", wait_until="domcontentloaded"
                    )
                    async with timeout(12):
                        data = await fut
                except TimeoutError:
                    await cleanup()
                    return None
                except Exception as e:
                    await cleanup()
                    print(f"Error: {e}")
                    return None
                finally:
                    page.remove_listener("request", get_payload)
                    await cleanup()
            await p.close()
            ret = "\n".join(data.splitlines()[2:]) if "Sources:" in data else data

            if "$@$" in ret:
                ret = ret[ret.index("$@$", 2) + 3 :]

            if "$~~~$" in ret:
                ret = ret[ret.index("$~~~$", 2) + 5 :]
            ret = ret.replace("<br>", "")
            ret = (
                ret.replace(", try unlimited chat https://www.blackbox.ai/", "")
                .replace("blackbox.ai", "honest.rocks")
                .replace("blackbox", "honest")
            )
            return ret

        return await execute()

    @cache()
    async def prompt(self, prompt: str, expert: str = "") -> tuple:
        _prompt = "You are being used as a chatbot for my discord bot do not return any html or any markdown or any json content just a string with the answer to the question asked"
        _prompt += f"\n{prompt}"
        data = await self._prompt(_prompt)
        if "[{" in data:
            obj, content = data.split("[", 1)[1].split("]$~~~$", 1)
            content = "\n".join(m for m in content.splitlines() if len(m) > 1)
            try:
                obj = json.loads(f"[{obj}]")
            except Exception:
                obj = {}
            return obj, content
        else:
            return ({}, data)
