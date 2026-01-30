# 导入必要的库
import ast  # 抽象语法树解析（当前未使用）
import json  # JSON数据处理
import requests  # HTTP请求库
import re  # 正则表达式

# 页面信息缓存文件路径
page_info_path = "./tmp/page_info.json"


# 目标B站视频URL
url = "https://www.bilibili.com/video/BV1rRGqzWEfR/?spm_id_from=333.337.search-card.all.click&vd_source=393172d5dc638338abf4db3a3cf9c4b7"

# 页面搜索技巧: 按F12打开开发者工具，在网络(Network)标签中搜索JSON响应，
# 查找包含 mp4、video、audio、play 等关键词的请求来定位视频资源

# 请求头配置，模拟浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
    "Referer": "https://www.bilibili.com/",  # 设置来源页面，避免防盗链
}


def info2local():
    """从B站获取视频页面信息并保存到本地文件"""
    # 发送HTTP请求获取页面内容
    response = requests.get(url, headers=headers)

    info_d = {}

    # 使用正则表达式提取视频标题
    match = re.search(r"<title>(.*?)_哔哩哔哩_bilibili</title>", response.text)
    title = match.group(1) if match else "custom#!+#-未知标题"

    # 从页面HTML中提取视频播放信息（包含视频和音频URL）
    match = re.search(
        r"<script>window.__playinfo__=(\{.*?\})</script>", response.text, re.S
    )
    playinfo = json.loads(match.group(1)) if match else None

    # 组装数据字典
    info_d["title"] = title
    info_d["playinfo"] = playinfo
    info_d["response_text"] = response.text

    # 将提取的信息保存到本地JSON文件
    with open(page_info_path, "w", encoding="utf-8") as f:
        json.dump(info_d, f, ensure_ascii=False, indent=2)


def local2info():
    """从本地文件读取已保存的视频信息"""
    with open(page_info_path, "r", encoding="utf-8") as f:
        playinfo = json.load(f)

    return playinfo


def parser(page_info):
    """解析视频信息，提取标题、视频URL和音频URL"""
    title = page_info["title"]
    # 从播放信息中提取视频流URL（取第一个，通常是最高质量）
    video_url = page_info["playinfo"]["data"]["dash"]["video"][0]["baseUrl"]
    # 从播放信息中提取音频流URL（取第一个，通常是最高质量）
    audio_url = page_info["playinfo"]["data"]["dash"]["audio"][0]["baseUrl"]

    return title, video_url, audio_url


def download(video_url, audio_url, title):
    """下载视频和音频文件到本地"""
    # 下载视频流数据（返回的是二进制数据字节流，需要用content属性获取）
    video_data = requests.get(video_url, headers=headers).content
    # 下载音频流数据
    audio_data = requests.get(audio_url, headers=headers).content

    # 保存视频文件
    with open(f"./tmp/{title}_video.mp4", "wb") as f:
        f.write(video_data)

    # 保存音频文件
    with open(f"./tmp/{title}_audio.mp3", "wb") as f:
        f.write(audio_data)


def merge(video, audio, title) -> None:
    """使用FFmpeg合并视频和音频文件"""
    # FFmpeg可执行文件路径（需要预先安装FFmpeg）
    ffmpeg_path = r"D:\tool\ffmpeg\bin\ffmpeg.exe"
    # 构建FFmpeg命令：-i 输入文件，-c copy 直接复制流不重新编码，-y 覆盖输出文件
    cmd = f'{ffmpeg_path} -i "{video}" -i "{audio}" -c copy "./target/{title}.mp4" -y'

    import os

    # 执行FFmpeg命令进行合并
    os.system(cmd)


def main():
    """主函数：执行视频下载和合并流程"""
    # 第一步：获取视频信息并保存到本地（首次运行时取消注释）
    # info2local()
    
    # 第二步：从本地文件读取视频信息
    page_info = local2info()
    
    # 第三步：解析视频信息，提取必要的URL和标题
    title, video_url, audio_url = parser(page_info)
    
    # 第四步：下载视频和音频文件（如需重新下载，取消注释）
    # download(video_url, audio_url, title)
    
    # 第五步：合并视频和音频文件为完整的MP4文件
    merge(f"./tmp/{title}_video.mp4", f"./tmp/{title}_audio.mp3", title)


if __name__ == "__main__":
    # 程序入口点
    main()
