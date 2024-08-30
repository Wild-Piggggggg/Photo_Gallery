from PIL import Image
import os
import concurrent.futures

def convert_image_to_webp(image_path):
    try:
        # 打开图像文件
        # image = Image.open(image_path)
        
        # 移除文件扩展名，生成新的 WebP 文件名
        new_filename = os.path.splitext(image_path)[0] + '.webp'
        print(new_filename)
        
        # 转换并保存为 WebP 格式
        # image.save(new_filename, 'webp')
        print(f"Converted {image_path} to {new_filename}")
    except Exception as e:
        print(f"Failed to convert {image_path}: {e}")

def convert_images_to_webp_async(directory):
    # 支持的图片格式列表
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')

    # 收集所有需要转换的文件路径
    image_paths = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.lower().endswith(supported_formats)]

    # 使用 ThreadPoolExecutor 进行异步并行处理
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(convert_image_to_webp, image_paths)

if __name__ == "__main__":
    # 获取当前目录
    current_directory = os.getcwd()
    convert_images_to_webp_async(current_directory)
