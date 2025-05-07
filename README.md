- [脚本合集](#脚本合集)
  - [概述（文件结构）](#概述文件结构)
  - [脚本使用说明](#脚本使用说明)
    - [split\_train\_val.py](#split_train_valpy)
    - [write\_img\_path.py](#write_img_pathpy)
    - [json\_to\_yolo.py](#json_to_yolopy)
    - [split\_files.py](#split_filespy)
    - [URL2mp4.py](#url2mp4py)


# 脚本合集

本仓库以个人应用为导向，总结学习与开发过程中应用到的脚本

## 概述（文件结构）

这里只提供一个功能概述，具体使用方法见下文

| 脚本               | 功能                                                         | 脚本链接                                                     |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| split_train_val.py | 划分数据集                                                   | [链接](https://github.com/bhsh0112/Script/blob/main/yolo/split_train_val.py) |
| write_img_path.py  | 按要求把文件路径保存到指定文件（yolo用）                     | [链接](https://github.com/bhsh0112/Script/blob/main/yolo/write_img_path.py) |
| json_to_yolo.py    | 对标注文件进行json到yolo的格式转换（yolo用）                 | [链接](https://github.com/bhsh0112/Script/blob/main/yolo/json_to_yolo.py) |
| split_files.py     | 把一个文件夹内的同类型文件等分到n个子文件夹中（常用于分配任务） | [链接](https://github.com/bhsh0112/Script/blob/main/split-files.py) |
| URL2mp4.py         | 下载链接中的视频（当前支持youtube和bilibili）                | [链接](https://github.com/bhsh0112/Script/blob/main/URL2mp4.py) |

## 脚本使用说明

### split_train_val.py

**作用：**划分数据集

```
python split_train_val.py
```

### write_img_path.py

**作用：**按要求把文件路径保存到指定文件

- 按照格式修改64行的路径

```
python write_img_path.py
```

### json_to_yolo.py

**作用：**对标注文件进行格式转换

- 按照格式修改55行对检测类别的列举

```
python json_to_yolo.py
```

### split_files.py

**作用：**把一个文件夹内的同类型文件等分到n个子文件夹中（常用于分配任务）

- 参数说明
  - source_dir：要分配的文件夹
  - file_extension：要分配文件的扩展名，例：.txt
  - num_folders：要等分成几份

```
python split_files.py --source_dir /path/to/folder --file_extension .[extension] --num_folders n
```

例：

```
python split_files.py --source_dir images file_extension .jpg --num_folders 5
```

### URL2mp4.py

**作用：**输入视频网站链接（当前支持bilibili和youtube），即可在当前目录下新建一个Downloads文件夹，保存链接中的视频

环境配置：

- `python -m pip install yt-dlp`
- 安装ffmpeg（不同系统或不同，可自查教程，通常单一指令即可）

```bash
python URL2mp4.mp4
```

运行后在终端输入URL即可
