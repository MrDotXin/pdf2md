from src.Config import config
from src.tools import paddleOCR
from src.tools import textin
import tqdm
import os

def lisFilesFromPath(folder_path):
    """
    使用os.walk获取文件夹中的所有文件及其路径，并抽取文件名称（不带后缀）
    """
    files_info = []
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # 获取文件名（不带后缀）
            file_name_without_extension = os.path.splitext(file)[0]
            
            files_info.append({
                'file_path': file_path,
                'file_name': file,  # 完整文件名
                'raw_file_name': file_name_without_extension
            })
    
    return files_info

def run() :
    save_dir = './tmp/textin/'
    benchmark = './benchmark/'
    files = lisFilesFromPath(benchmark)
    
    for file in tqdm.tqdm(files) :
        target_dir = os.path.join(save_dir, file['raw_file_name'])
        if not os.path.exists(target_dir) :
            os.makedirs(target_dir)
        textin.convert(file['file_path'], target_dir)
        
if __name__ == "__main__" :
    run()