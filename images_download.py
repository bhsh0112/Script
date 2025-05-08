import urllib3
import os
from urllib.parse import urljoin, urlparse

# 第一个函数，用来下载网页，返回网页内容
def download_content(url):
    http = urllib3.PoolManager()
    response = http.request("GET", url)
    return response.data

# 将字符串内容保存到文件中
def save_to_file(filename, content):
    print(filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # 确保文件夹存在
    with open(filename, "wb") as fo:  # 使用二进制写入方式保存字节内容
        fo.write(content)

url = input("请输入网址:")
save_path = input("请输入保存路径:")
result = download_content(url)
tmp_html_path="./tmp_for_download_images.html"
save_to_file(tmp_html_path, result)

from bs4 import BeautifulSoup

# 输入参数为要分析的 html 文件名，返回值为对应的 BeautifulSoup 对象
def create_doc_from_filename(filename):
    with open(filename, "r", encoding='utf-8') as fo:
        html_content = fo.read()
    doc = BeautifulSoup(html_content, "lxml")
    return doc

doc = create_doc_from_filename(tmp_html_path)
images = doc.find_all("img")

# 下载图片
def download_images(url, images,save_path):
    os.makedirs(save_path, exist_ok=True)  # 确保文件夹存在
    for i in images:
        src = i.get("src")  # 使用 get 方法更安全
        if not src:
            continue

        # 将相对URL转换为绝对URL
        src = urljoin(url, src)

        # 获取图片的文件名
        parsed_url = urlparse(src)
        file_name = os.path.basename(parsed_url.path)

        # 下载图片
        try:
            http = urllib3.PoolManager()
            response = http.request("GET", src)
            if response.status >= 200 and response.status < 300:
                with open(os.path.join(save_path, file_name), "wb") as f:
                    f.write(response.data)
                print(f"已下载: {file_name}")
            else:
                print(f"下载图片时出错，HTTP状态码: {response.status}")
        except Exception as e:
            print(f"下载图片时出错: {e}")

download_images(url, images,save_path)

try:
    os.remove(tmp_html_path)
    print(f"文件 '{tmp_html_path}' 已删除。")
except FileNotFoundError:
    print(f"文件 '{tmp_html_path}' 不存在，无法删除。")
except PermissionError:
    print(f"没有权限删除文件 '{tmp_html_path}'。")
except Exception as e:
    print(f"删除文件时出错: {e}")