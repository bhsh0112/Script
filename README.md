- [脚本合集](#脚本合集)
  - [概述（文件结构）](#概述文件结构)
  - [脚本使用说明](#脚本使用说明)
    - [split\_train\_val.py](#split_train_valpy)
    - [write\_img\_path.py](#write_img_pathpy)
    - [json\_to\_yolo.py](#json_to_yolopy)
    - [split\_files.py](#split_filespy)



## 脚本合集

本仓库以个人应用为导向，总结学习与开发过程中应用到的脚本

### 概述（文件结构）

- yolo：yolo相关的脚本
  - split_train_val.py：数据集划分
  - write_img_path.py：文件路径写入
  - json_to_yolo.py：标注文件格式转换
- split_files.py：文件均分

### 脚本使用说明

#### split_train_val.py

**作用：**划分数据集

```
python split_train_val.py
```

#### write_img_path.py

**作用：**按要求把文件路径保存到指定文件

- 按照格式修改64行的路径

```
python write_img_path.py
```

#### json_to_yolo.py

**作用：**对标注文件进行格式转换

- 按照格式修改55行对检测类别的列举

```
python json_to_yolo.py
```

#### split_files.py

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

