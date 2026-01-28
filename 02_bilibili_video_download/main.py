import json
import requests
import re


page_info_path = "./tmp/page_info.json"


url = "https://www.bilibili.com/video/BV1rRGqzWEfR/?spm_id_from=333.337.search-card.all.click&vd_source=393172d5dc638338abf4db3a3cf9c4b7"

# 页面搜索: f12 网络 json中:  mp4 video audio play 等关键词用于定位

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
    "Referer": "https://www.bilibili.com/",
}


def info2local():
    response = requests.get(url, headers=headers)

    info_d = {}

    match = re.search(r"<title>(.*?)_哔哩哔哩_bilibili</title>", response.text)
    title = match.group(1) if match else "custom#!+#-未知标题"

    match = re.search(
        r"<script>window.__playinfo__=(\{.*?\})</script>", response.text, re.S
    )
    playinfo = json.loads(match.group(1)) if match else None

    info_d["title"] = title
    info_d["playinfo"] = playinfo
    info_d["response_text"] = response.text

    with open(page_info_path, "w", encoding="utf-8") as f:
        json.dump(info_d, f, ensure_ascii=False, indent=2)


def local2info():
    with open(page_info_path, "r", encoding="utf-8") as f:
        playinfo = json.load(f)

    return playinfo


def parser(page_info):
    title = page_info["title"]
    video_url = page_info["playinfo"]["data"]["dash"]["video"][0]["baseUrl"]
    audio_url = page_info["playinfo"]["data"]["dash"]["audio"][0]["baseUrl"]

    return title, video_url, audio_url


def main():
    info2local()
    page_info = local2info()
    title, video_url, audio_url = parser(page_info)
    print(f"{title=}, {video_url=}, {audio_url=}")


if __name__ == "__main__":
    main()
