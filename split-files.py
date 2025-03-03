import os
import shutil
import argparse

def distribute_files(source_dir, file_extension, num_folders):
    """
    将指定文件夹中的特定类型文件均匀分配到多个子文件夹中。

    :param source_dir: 包含文件的源文件夹路径
    :param file_extension: 需要处理的文件扩展名（例如 ".txt"）
    :param num_folders: 要划分的文件夹数量
    """
    # 获取源文件夹中所有指定类型的文件
    files = [f for f in os.listdir(source_dir) if f.endswith(file_extension)]
    total_files = len(files)

    if total_files == 0:
        print(f"没有找到扩展名为 {file_extension} 的文件。")
        return

    # 计算每个文件夹应分配的文件数量
    files_per_folder = total_files // num_folders
    remaining_files = total_files % num_folders

    print(f"总文件数: {total_files}")
    print(f"每个文件夹分配文件数: {files_per_folder}")
    print(f"剩余文件数: {remaining_files}")

    # 创建目标文件夹
    for i in range(num_folders):
        folder_name = os.path.join(source_dir, f"Folder_{i + 1}")
        os.makedirs(folder_name, exist_ok=True)
        print(f"创建文件夹: {folder_name}")

    # 分配文件到文件夹
    folder_index = 0
    for file in files:
        source_file_path = os.path.join(source_dir, file)
        target_folder = os.path.join(source_dir, f"Folder_{folder_index + 1}")
        target_file_path = os.path.join(target_folder, file)

        shutil.move(source_file_path, target_file_path)
        print(f"移动文件 {file} 到 {target_folder}")

        folder_index += 1
        if folder_index >= num_folders:
            folder_index = 0

    print("文件分配完成！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将大量同类型文件均匀分配到多个文件夹中")
    parser.add_argument("--source_dir", type=str, help="源文件夹路径")
    parser.add_argument("--file_extension", type=str, help="文件扩展名（例如 '.txt'）")
    parser.add_argument("--num_folders", type=int, help="要划分的文件夹数量")

    args = parser.parse_args()

    distribute_files(args.source_dir, args.file_extension, args.num_folders)