import requests
import re
import json


url = "https://www.acfun.cn/v/ac48226867"


# 请求头配置，模拟浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
    "Referer": "https://www.acfun.cn/",  # 设置来源页面，避免防盗链
}


def info2local():
    """从AcFun获取视频页面信息并保存到本地文件"""
    # 发送HTTP请求获取页面内容
    rsp = requests.get(url, headers=headers)

    info_d = {}

    # 从页面HTML中提取视频播放信息（包含视频和音频URL）
    match = re.search(r"window.pageInfo = window.videoInfo = (.*?);", rsp.text)
    page_info = json.loads(match.group(1)) if match else {}
    title = page_info.get("title", "未知标题")
    info_d["title"] = title
    info_d["page_info"] = page_info
    info_d["response_text"] = rsp.text

    # 将提取的信息保存到本地JSON文件
    with open("./tmp/page_info.json", "w", encoding="utf-8") as f:
        json.dump(info_d, f, ensure_ascii=False, indent=2)


def local2info():
    """从本地文件读取已保存的视频信息"""
    with open("./tmp/page_info.json", "r", encoding="utf-8") as f:
        page_info = json.load(f)

    return page_info


def main():
    # info2local()
    info = local2info()

    ksPlayJson = info["page_info"]["currentVideoInfo"]["ksPlayJson"]

    ks_play_d = json.loads(ksPlayJson)

    video_url_m3u8 = ks_play_d["adaptationSet"][0]["representation"][0]["backupUrl"][0]

    print(video_url_m3u8)

    rsp_text = requests.get(video_url_m3u8, headers=headers).text

    # 提取所有的分段视频URL
    matches = re.findall(r"#EXTINF:5\.000000,[\r\n]+([^\r\n]+)", rsp_text)


    # 存在于ks_play_d["adaptationSet"][0]["representation"][0]["url"] 中. (前缀)
    bash_url = "https://ali-safety-video.acfun.cn/mediacloud/acfun/acfun_video/"

    with open(f'./target/{info["title"]}.mp4', "wb+") as f:

        for i in matches:
            url = bash_url + i
            f.write(requests.get(url, headers=headers).content)

    



if __name__ == "__main__":
    main()
