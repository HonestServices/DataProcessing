from typing import Any
from urllib.parse import quote, unquote

from pydantic import BaseModel

from .token import TokenManager
from .utils import get_timestamp


# Model
class BaseRequestModel(BaseModel):
    WebIdLastTime: str = str(get_timestamp("sec"))
    aid: str = "1988"
    app_language: str = "en"
    app_name: str = "tiktok_web"
    browser_language: str = "en-US"
    browser_name: str = "Mozilla"
    browser_online: str = "true"
    browser_platform: str = "Win32"
    browser_version: str = quote(
        "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        safe="",
    )
    channel: str = "tiktok_web"
    cookie_enabled: str = "true"
    device_id: int = 7475778369566443039
    device_platform: str = "web_pc"
    focus_state: str = "true"
    from_page: str = "user"
    history_len: int = 4
    is_fullscreen: str = "false"
    is_page_visible: str = "true"
    language: str = "en"
    os: str = "windows"
    priority_region: str = ""
    referer: str = ""
    region: str = "US"  # SG JP KR...
    root_referer: str = quote("https://www.tiktok.com/", safe="")
    screen_height: int = 1080
    screen_width: int = 1920
    webcast_language: str = "en"
    tz_name: str = quote("America/New_York", safe="")
    # verifyFp: str = VerifyFpManager.gen_verify_fp()
    msToken: str = TokenManager.gen_real_msToken()


# router model
class UserProfile(BaseRequestModel):
    secUid: str = ""
    uniqueId: str


class UserPost(BaseRequestModel):
    coverFormat: int = 2
    count: int = 35
    cursor: int = 0
    secUid: str


class UserLike(BaseRequestModel):
    coverFormat: int = 2
    count: int = 30
    cursor: int = 0
    secUid: str


class UserCollect(BaseRequestModel):
    cookie: str = ""
    coverFormat: int = 2
    count: int = 30
    cursor: int = 0
    secUid: str


class UserPlayList(BaseRequestModel):
    count: int = 30
    cursor: int = 0
    secUid: str


class UserMix(BaseRequestModel):
    count: int = 30
    cursor: int = 0
    mixId: str


class PostDetail(BaseRequestModel):
    itemId: str


class PostComment(BaseRequestModel):
    aweme_id: str
    count: int = 20
    cursor: int = 0
    current_region: str = "US"


# yayayayaya (Post Comment Reply)
class PostCommentReply(BaseRequestModel):
    item_id: str
    comment_id: str
    count: int = 20
    cursor: int = 0
    current_region: str = "US"


# yayaya (User Fans)
class UserFans(BaseRequestModel):
    secUid: str
    count: int = 30
    maxCursor: int = 0
    minCursor: int = 0
    scene: int = 67


# yayaya (User Follow)
class UserFollow(BaseRequestModel):
    secUid: str
    count: int = 30
    maxCursor: int = 0
    minCursor: int = 0
    scene: int = 21
