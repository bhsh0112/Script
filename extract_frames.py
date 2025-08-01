import cv2
import os
import argparse

def extract_frames(video_path, start_sec, end_sec, n_fps, output_dir):
    # 检查视频文件是否存在
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"视频文件不存在: {video_path}")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.basename(video_path)
    
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError("无法打开视频文件")
    
    # 获取视频属性
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    if end_sec==-1:
        end_sec = duration
    
    # 验证时间范围有效性
    if start_sec < 0 or end_sec > duration or start_sec >= end_sec:
        cap.release()
        raise ValueError(f"无效时间范围 (视频时长: {duration:.2f}秒)")
    
    # 将秒转换为帧号
    start_frame = int(start_sec * fps)
    end_frame = min(int(end_sec * fps), total_frames - 1)
    
    # 计算帧间隔
    interval = max(1, int(round(fps / n_fps)))  # 至少间隔1帧
    
    print(f"视频信息: {total_frames} 帧, FPS: {fps:.2f}, 时长: {duration:.2f}秒")
    print(f"抽帧范围: {start_sec:.2f}秒 - {end_sec:.2f}秒 (帧 {start_frame}-{end_frame})")
    print(f"抽帧设置: 每秒 {n_fps} 帧 (间隔: {interval} 帧)")
    
    # 定位到起始帧
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    count = 0
    saved_count = 0
    current_frame = start_frame
    
    while current_frame <= end_frame:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 检查是否达到保存间隔
        if count % interval == 0:
            # 计算当前时间戳
            timestamp = current_frame / fps
            frame_path = os.path.join(output_dir, filename+f"_frame_{timestamp:.2f}s.jpg")
            cv2.imwrite(frame_path, frame)
            saved_count += 1
        
        count += 1
        current_frame += 1
    
    cap.release()
    print(f"完成! 共保存 {saved_count} 张图像到: {output_dir}")
    return saved_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="视频抽帧工具 - 按秒数指定范围",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--video_path", default="D:\\麒纪\\yolo广告检测\\超三联赛-广告数据提取\\广告2\\广告2.mp4",help="输入MP4视频路径")
    parser.add_argument("--start_sec", type=float, help="起始时间(秒)")
    parser.add_argument("--end_sec", type=float, help="结束时间(秒)")
    parser.add_argument("--n_fps", type=int, help="每秒抽取帧数")
    parser.add_argument("--output_dir",default="output1", help="输出目录路径")

    args = parser.parse_args()
    
    try:
        extract_frames(
            video_path=args.video_path,
            start_sec=args.start_sec,
            end_sec=args.end_sec,
            n_fps=args.n_fps,
            output_dir=args.output_dir
        )
    except Exception as e:
        print(f"错误: {str(e)}")