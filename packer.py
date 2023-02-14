# Code by: utf-8 
# Sinbing 2023-2-14
import os
import sys
import shutil
import zipfile


# init.
if hasattr(sys, "_MEIPASS"):
    DEBUG = False
else:
    DEBUG = True
    print('=====================\n 警告! 你正在DEBUG \n=====================')


def resource_path(filaeName):
    if not DEBUG:
        return os.path.join(sys._MEIPASS, filaeName)
    return os.path.join(filaeName)


def Dprint(text: str):
    if DEBUG:
        print(text)

def getJarFile(file_path: str):
    full_file_list = os.listdir(file_path)
    Dprint(f'DEBUG | 程序目录下完整文件列表: {full_file_list}')

    for item in full_file_list:
        Dprint(f'DEBUG | 在在处理文件: {item}')
        file_name, file_ext = os.path.splitext(item)
        if file_ext == '.jar':
            return file_name


def unzipjarFile(script_path: str, jar_file_name: str):
    unzip_flag = False

    temp_file = os.path.join(script_path, 'temp')
    if not os.path.exists(temp_file):
        os.makedirs(temp_file)
        try:
            jar_file = zipfile.ZipFile(os.path.join(script_path, jar_file_name+'.jar'), "r")
            for item in jar_file.namelist(): 
                Dprint(f'DEBUG | 提取JAR中文件: {item}')
                jar_file.extract(item, temp_file)
            unzip_flag = True

        except:
            print('ERROR | 从JAR提取文件时发生错误')
    else:
        print('WARING| 存在临时文件夹，程序中止')
    return temp_file, unzip_flag


def recoverFile(work_path: str):
    lang_file_list = os.listdir(resource_path(os.path.join('lang')))
    work_dir_list = os.listdir(os.path.join(work_path, 'assets'))
    print(f'INFO  | 已读取语言文件: {lang_file_list}\nDEBUG | MOD中包含: {work_dir_list}')

    try:
        for dir_name in work_dir_list:
            if dir_name in lang_file_list:
                for lang_file in os.listdir(resource_path(os.path.join('lang', dir_name, 'lang'))):
                    shutil.copy2( \
                    resource_path(os.path.join('lang', dir_name, 'lang', lang_file)), \
                    os.path.join(work_path, 'assets', dir_name, 'lang', lang_file))
                    print(f'INFO | 成功向[{dir_name}]中添加语言文件[{lang_file}]')
    except:
        print('ERROR | 向JAR添加汉化文件时发生错误')
        return False
    return True


def reJarFile(zip_path: str, work_path: str, file_name: str):
    jarFile = zipfile.ZipFile(os.path.join(work_path, f'汉化-{file_name}_zh_CN.jar'), 'w')

    for path, dir_list, file_list in os.walk(zip_path):  
        for file_name in file_list:  
            Dprint(f'DEBUG | 添加文件至压缩: {os.path.join(path, file_name)}')
            jarFile.write(os.path.join(path, file_name), zipfile.ZIP_DEFLATED)
    jarFile.close()

    os.remove(zip_path)


if __name__ == '__main__':
    script_path = os.path.split(os.path.realpath(__file__))[0]
    jar_file_name = getJarFile(script_path)
    print(f'INFO  | 成功获取到MOD文件{jar_file_name}'+'.jar')
    
    unzip_path, unzip_flag = unzipjarFile(script_path, jar_file_name)
    Dprint(f'DEBUG | 解压至临时目录: {unzip_path}')
    if not unzip_flag:
        input('\n    按下回车退出...')
        exit(0)
    else:
        if not recoverFile(unzip_path):
            input('\n    按下回车退出...')
            exit(0)
        else:
            reJarFile(unzip_path, script_path, jar_file_name)
