import json
import random
import re
from typing import Optional, Union

from aiohttp import ClientSession
from redis.asyncio import Redis

from .._impl.Twitter.twitter import TweetNotFound, UserNotFound, UserSuspended
from ..models.Twitter import Tweet, Tweets, TwitterUser
from ..utils import get_random_string
from .Base import BaseService, cache

REQUEST_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
REQUEST_PLATFORMS = ["Linux", "Windows"]
HEADERS = {
    "Cookie": 'guest_id=v1%3A173612475719932019; kdt=oJYgBMZ9CGAkM8NFGtVrC27Ga4tHh8zIZXanJbGC; auth_token=6dd141f0f70c570e140bfc79ff4f05aba21c7da5; dnt=1; twid=u%3D1499214330172252165; guest_id_marketing=v1%3A173612475719932019; guest_id_ads=v1%3A173612475719932019; __cf_bm=tukzuVHE8GBK6t4zvalOUUnncF4nbhX9JymMs4LrfK4-1742832732-1.0.1.1-irRK4EhsliqGXeL7j2SmqslvgsCUY4gvEKAi5NXdR7WL5xJojDASn616E8bp0WnjNeO0rreZ0JmI1S4I7SA8JBFssPIuc32i3S0Ina336zE; lang=en; d_prefs=MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; personalization_id="v1_U8mniGmDGiGkseSdh5k88w=="; ct0=c93b1c9d3a9439b5cd17af161a11f3c1b9b012a65aa26793e0913f44cf56810f951b39733e66a32fc4a0888abc7ecef3bcfe2090fd0a43476e5750bbd915e8cbb89ca9cb01e2fa127f97ce1e6727244f',
    "Sec-Ch-Ua": """Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134""",
    "X-Twitter-Client-Language": "en",
    "X-Csrf-Token": "c93b1c9d3a9439b5cd17af161a11f3c1b9b012a65aa26793e0913f44cf56810f951b39733e66a32fc4a0888abc7ecef3bcfe2090fd0a43476e5750bbd915e8cbb89ca9cb01e2fa127f97ce1e6727244f",
    "Sec-Ch-Ua-Mobile": "?0",
    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
    "X-Twitter-Auth-Type": "OAuth2Session",
    "X-Twitter-Active-User": "yes",
    "Sec-Ch-Ua-Platform": """Windows""",
    "Accept": "*/*",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://twitter.com/nxyylol",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}


class TwitterService(BaseService):
    def __init__(self: "TwitterService", redis: Redis, ttl: Optional[int] = None):
        self.redis = redis
        self.ttl = ttl
        super().__init__(self.redis, self.ttl)

    @cache()
    async def get_guest_token(self: "TwitterService") -> str:
        async with ClientSession() as session:
            async with session.request(
                "POST", "https://api.x.com/1.1/guest/activate.json", headers=HEADERS
            ) as response:
                data = await response.json()

        return data["guest_token"]

    def get_csrf_token(self: "TwitterService") -> str:
        return get_random_string(32)

    async def fetch_tweet(self: "TwitterService", url: str) -> Tweet:
        try:
            tweet_id = re.search(r"status/(\d+)", url).group(1)
        except AttributeError:
            raise TweetNotFound(url)
        async with ClientSession() as session:
            async with session.get(
                "https://cdn.syndication.twimg.com/tweet-result",
                params={"id": tweet_id, "lang": "en", "token": "4ds4bk3f3r"},
            ) as response:
                data = await response.read()
        return Tweet.parse_raw(data)

    async def fetch_user(
        self: "TwitterService", username: str, raw: Optional[bool] = False
    ) -> Union[TwitterUser, dict]:
        async with ClientSession() as session:
            async with session.get(
                "https://twitter.com/i/api/graphql/mCbpQvZAw6zu_4PvuAUVVQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22"
                + username
                + "%22%2C%22withSafetyModeUserFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%7D",
                headers=HEADERS,
            ) as response:
                if response.status == 404:
                    raise UserNotFound(username)
                data = await response.json()
                if raw:
                    return data
            user = TwitterUser(**data)
        if reason := user.data.user.result.reason:
            if reason == "Suspended":
                raise UserSuspended(username)
        if not user.data.user.result.id and not user.data.user.result.reason:
            raise UserNotFound(username)
        return user
