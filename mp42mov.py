import os
import subprocess
from moviepy.editor import VideoFileClip
from PIL import Image

def convert_to_live_photo(input_video, output_prefix, duration=3.0, keyframe_time=0.5):
    """
    将视频片段转换为实况照片（JPEG + MOV）
    
    参数:
    input_video: 输入视频文件路径
    output_prefix: 输出文件前缀（不含扩展名）
    duration: 实况照片总时长（秒）
    keyframe_time: 关键帧时间点（秒）
    """
    # 临时文件路径
    temp_video = "temp_cropped.mp4"
    temp_keyframe = "temp_keyframe.jpg"
    
    try:
        # 1. 裁剪视频到指定时长
        clip = VideoFileClip(input_video)
        if clip.duration < duration:
            print(f"警告: 视频长度({clip.duration:.1f}s)小于目标时长({duration}s)")
            duration = clip.duration
        
        # 确保关键帧在有效范围内
        keyframe_time = min(max(keyframe_time, 0.1), duration - 0.1)
        
        # 裁剪视频
        sub_clip = clip.subclip(0, duration)
        sub_clip.write_videofile(
            temp_video, 
            codec="libx264", 
            audio_codec="aac",
            fps=30,
            preset='fast',
            logger=None
        )
        sub_clip.close()
        clip.close()
        
        # 2. 提取关键帧作为封面
        keyframe_clip = VideoFileClip(input_video).subclip(keyframe_time, keyframe_time+0.1)
        keyframe_clip.save_frame(temp_keyframe, t=0)
        keyframe_clip.close()
        
        # 3. 转换视频为MOV格式（苹果Live Photo兼容格式）
        output_mov = f"{output_prefix}.mov"
        output_jpg = f"{output_prefix}.jpg"
        
        subprocess.run([
            "ffmpeg", "-y", "-i", temp_video,
            "-c:v", "libx264", "-profile:v", "main",
            "-level", "3.1", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            output_mov
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 4. 保存关键帧为JPEG
        img = Image.open(temp_keyframe)
        img.save(output_jpg, "JPEG", quality=95)
        
        print(f"转换成功！生成文件:")
        print(f"- 实况照片封面: {output_jpg}")
        print(f"- 实况照片视频: {output_mov}")
        
    except Exception as e:
        print(f"转换失败: {str(e)}")
    finally:
        # 清理临时文件
        for f in [temp_video, temp_keyframe]:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    # 使用示例
    input_video = "C:\\Users\\27265\Desktop\\tmp\Script\\test\\46a04f5618757cfa9f15d3a6b81681ee.mp4"
    output_prefix = "test\\test"  # 输出文件名前缀
    
    convert_to_live_photo(
        input_video,
        output_prefix,
        duration=3.0,      # 实况照片时长(建议3秒)
        keyframe_time=1.0  # 封面帧时间点
    )