# 导入所需的库
import os
import yt_dlp

def download_youtube_video(url):
    try:
        # 设置下载选项
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': os.path.join(os.getcwd(), 'Downloads', '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'quiet': False
        }
        
        # 创建下载目录（如果不存在）
        download_dir = os.path.join(os.getcwd(), 'Downloads')
        os.makedirs(download_dir, exist_ok=True)
        
        # 下载视频
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"正在下载: {url}")
            ydl.download([url])
        
        print("\n下载完成！视频已保存到: Downloads 文件夹")
        
    except Exception as e:
        print(f"下载过程中发生错误: {e}")

def progress_hook(d):
    """
    监控下载进度
    """
    if d['status'] == 'downloading':
        print(f"正在下载: {d['_percent_str']} 已下载: {d['_total_bytes_str']}", end='\r')
    elif d['status'] == 'finished':
        print("\n下载完成！正在处理合并文件...")

if __name__ == "__main__":
    # 获取用户输入的URL
    url = input("请输入YouTube视频的URL: ")
    
    # 下载视频
    download_youtube_video(url)