import json
import requests
import re

url = "https://www.bilibili.com/video/BV1rRGqzWEfR/?spm_id_from=333.337.search-card.all.click&vd_source=393172d5dc638338abf4db3a3cf9c4b7"

# 页面搜索: f12 网络 json中:  mp4 video audio play 等关键词用于定位

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
    "Referer": "https://www.bilibili.com/",
}


def info2local():
    response = requests.get(url, headers=headers)

    match = re.search(r"<title>(.*?)_哔哩哔哩_bilibili</title>", response.text)
    title = match.group(1) if match else "custom#!+#-未知标题"

    match = re.search(
        r"<script>window.__playinfo__=(\{.*?\})</script>", response.text, re.S
    )
    playinfo_json = json.loads(match.group(1)) if match else None

    with open(
        "./02_bilibili_video_download/response.text.html", "w", encoding="utf-8"
    ) as f:
        f.write(response.text)

    with open("./02_bilibili_video_download/playinfo.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(playinfo_json, ensure_ascii=False, indent=2))


def local2info():
    with open("./02_bilibili_video_download/playinfo.json", "r", encoding="utf-8") as f:
        playinfo = json.load(f)

    return playinfo


def parser(playinfo):
    video_url = playinfo["data"]["dash"]["video"][0]["baseUrl"]
    audio_url = playinfo["data"]["dash"]["audio"][0]["baseUrl"]

    return video_url, audio_url


if __name__ == "__main__":
    playinfo = local2info()
    video_url, audio_url = parser(playinfo)
    print("video_url:", video_url)
    print("audio_url:", audio_url)
