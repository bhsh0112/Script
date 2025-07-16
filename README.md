# 脚本合集

本仓库以个人应用为导向，总结学习与开发过程中应用到的脚本

## 1 概述（文件结构）

这里只提供一个功能概述，具体使用方法见下文

| 脚本（跳转说明）       | 功能                                                         | 脚本链接                                                     | 脚本运行说明                                          |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| split_train_val.py | 划分数据集                                                   | [脚本代码](https://github.com/bhsh0112/Script/blob/main/yolo/split_train_val.py) | [split_train_val.py](#21-split_train_valpy) |
| write_img_path.py  | 按要求把文件路径保存到指定文件（yolo用）                     | [脚本代码](https://github.com/bhsh0112/Script/blob/main/yolo/write_img_path.py) | [write_img_path.py](#22-write_img_pathpy) |
| json_to_yolo.py    | 对标注文件进行json到yolo的格式转换（yolo用）                 | [脚本代码](https://github.com/bhsh0112/Script/blob/main/yolo/json_to_yolo.py) | [json_to_yolo.py](#23-json_to_yolopy) |
| split_files.py     | 把一个文件夹内的同类型文件等分到n个子文件夹中（常用于分配任务） | [脚本代码](https://github.com/bhsh0112/Script/blob/main/split-files.py) | [split_files.py](#24-split_filespy) |
| URL2mp4.py         | 下载链接中的视频（当前支持youtube和bilibili）                | [脚本代码](https://github.com/bhsh0112/Script/blob/main/URL2mp4.py) | [URL2mp4.py](#25-url2mp4py) |
| Images_download.py | 批量下载链接中的图片                                         | [脚本代码](https://github.com/bhsh0112/Script/blob/main/images_download.py) | [Images_download.py](#26-images_downloadpy) |
| geojson_to_sql.py  | 把geojson文件转为mysql写入语句                              | [脚本代码](https://github.com/bhsh0112/Script/blob/zbtbl/zbtbl/geojson_to_sql.py) | [geojson_to_sql.py](#27-geojson_to_sqlpy) |
| mysql_edit.py      | 远程连接mysql数据库并批量编辑                                | [脚本代码](https://github.com/bhsh0112/Script/blob/zbtbl/zbtbl/mysql_edit.py) | [mysql_edit.py](#28-mysql_editpy) |
| tb_crawler.py      | 模拟浏览操作爬取淘宝商品列表                                 | [脚本代码](https://github.com/bhsh0112/Script/blob/zbtbl/zbtbl/tb_crawler.py) | [tb_crawler.py](#29-tb_crawlerpy) |
| calligraphy        | 一些视觉相关的识别、变换、裁切、提取                          | [脚本代码](https://github.com/bhsh0112/Script/tree/zbtbl/zbtbl/calligraphy) | [calligraphy](#210-calligraphy) |
| mp42gif.py | MP4转gif | [脚本代码](https://github.com/bhsh0112/Script/blob/sh/mp42gif.py) | [mp42gif.py](#211-mp42gifpy) |
| label_vis.py | yolo标注文件可视化 | [脚本代码](https://github.com/bhsh0112/Script/blob/main/yolo/label_vis.py) | [label_vis.py](#212-label_vispy) |

## 2 脚本使用说明

### 2.1 split_train_val.py

**作用：** 划分数据集

**代码运行：**

```
python split_train_val.py
```

### 2.2 write_img_path.py

**作用：** 按要求把文件路径保存到指定文件

**前期准备：**

- 按照格式修改64行的路径

```
python write_img_path.py
```

### 2.3 json_to_yolo.py

**作用：** 对标注文件进行格式转换

**前期准备：**

- 按照格式修改55行对检测类别的列举

**代码运行：**

```
python json_to_yolo.py
```

### 2.4 split_files.py

**作用：** 把一个文件夹内的同类型文件等分到n个子文件夹中（常用于分配任务）

**前期准备：** 需要修改代码参数

- 参数说明
  - source_dir：要分配的文件夹
  - file_extension：要分配文件的扩展名，例：.txt
  - num_folders：要等分成几份

**代码运行：**

```
python split_files.py --source_dir /path/to/folder --file_extension .[extension] --num_folders n
```

例：

```
python split_files.py --source_dir images file_extension .jpg --num_folders 5
```

### 2.5 URL2mp4.py

**作用：** 输入视频网站链接（当前支持bilibili和youtube），即可在当前目录下新建一个Downloads文件夹，保存链接中的视频

**前期准备：** 根据以下说明配置环境

- `python -m pip install yt-dlp`
- 安装ffmpeg（不同系统或不同，可自查教程，通常单一指令即可）

**代码运行：**

```bash
python URL2mp4.mp4
```

运行后在终端输入URL即可

### 2.6 images_download.py

**作用：** 输入网站链接及保存路径，即可将网站链接中的所有图片保存到输入的保存路径下

**前期准备：** 根据以下说明配置环境

```
pip install urllib3
pip install bs4
```

**代码运行：**

```
python images_download.py
```

运行后输入URL及保存地址

### 2.7 geojson_to_sql.py

- zhengbantubalu

**作用：** 把geojson文件转换成sql写入语句

**前期准备：** 需要修改代码参数，一大堆参数，一个不对都不能跑

目前没有通用化和交互，只能手动改硬编码参数，仅支持我自己的项目

### 2.8 mysql_edit.py

- zhengbantubalu

**作用：** 通过python远程连接mysql数据库，进行少量修改操作

**前期准备：** 根据代码里用到的库自行安装

仍然是硬编码，作为数据库远程连接和修改脚本的小样

### 2.9 tb_crawler.py

- zhengbantubalu

**作用：** 通过自动化模拟操作edge浏览器浏览淘宝网页，爬取淘宝商品列表信息，存入mysql数据库

**前期准备：** 根据代码里用到的库自行安装

代码中硬编码了页面元素的指纹，导致只能在当时刚写好时用，淘宝一更新就用不了了，虽然说现在也用不上了，作为爬虫脚本和数据库脚本小样

### 2.10 calligraphy

- zhengbantubalu

**作用：**

- scan：调用摄像头识别纸张四角进行透视变换，之后二值化
- cut：将扫描好的6个汉字的字帖图片切割为每个汉字一张图片
- get：在每个汉字一张图片上提取出汉字笔画矢量

**前期准备：**

```
pip install -r requirements.txt
```

当时捣鼓opencv的实验品，跑通之后就转到java了，这个就没再管了。当时是在Ubuntu上跑的。只支持我的6个字一页的字帖，位置也不能变

### 2.11 mp42gif.py

**作用：**将输入的mp4转为gif，可以用于ppt制作，表情包制作等，支持设置输入路径、输出路径、起止时间和帧率

**前期准备：**

```
pip install moviepy
```

**代码运行：**

```
python mp42gif.py --start start_time --end end_time --fps fps
```

例：

默认转换整个视频，帧率为10
```
python mp42gif.py 
```
完整设置参数的运行指令如下：
```
python mp42gif.py --start 2.1 --end 7 --fps 10
```

### 2.12 label_vis.py

**作用：**可视化yolo格式的标注文件，标出标注框

**前期准备：**

```
pip install opencv-python numpy glob argparse
```

**代码运行：**

```
python label_vis.py --anbatations path/to/labels --images path/to/images --output path/to/output --suffix "(后缀)" --class_names "class1 class2(空格分隔)"
```

例：

默认输出到当前目录下的`label_output`文件夹中，后缀是"_annotated"

```
python label_vis.py --annotations ./data/dataset/labels --iamges ./data/dataset/images --class_names "car truck people"
```