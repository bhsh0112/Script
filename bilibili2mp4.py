import os
import re
from urllib.parse import urlparse

def download_bilibili_video(url):
    """
    下载哔哩哔哩视频

    参数:
        url (str): 哔哩哔哩视频的URL
    """
    # 检查链接是否有效
    if not url:
        print("请输入有效的视频链接！")
        return

    # 检查链接是否为B站链接
    parsed_url = urlparse(url)
    if parsed_url.netloc not in ['www.bilibili.com', 'b23.tv']:
        print("请输入有效的B站视频链接！")
        return

    # 提取视频的BV号或AV号
    pattern = r"(?:BV|AV)(\d+)"
    match = re.search(pattern, url)
    if not match:
        print("无法从链接中提取视频ID！")
        return
    video_id = match.group()

    # 构建下载命令
    download_cmd = f"bbdown {url}"

    # 下载视频
    print(f"正在下载视频：{video_id}")
    os.system(download_cmd)
    print(f"视频 {video_id} 下载完成！")

if __name__ == "__main__":
    # 获取用户输入的URL
    url = input("请输入B站视频的URL: ")
    download_bilibili_video(url)