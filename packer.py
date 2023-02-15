# Code by: utf-8 
# Sinbing 2023-2-14
import os
import sys
import shutil
import zipfile


# init.
class colors:
    RED       = '\033[31;1m'
    GREEN     = '\033[32;1m'
    YELLOW    = '\033[33;1m'
    CYAN      = '\033[36;1m'


if hasattr(sys, "_MEIPASS"):
    DEBUG = False
else:
    DEBUG = True
    print(colors.YELLOW+ '=====================\n 警告! 你正在DEBUG \n=====================')


def Log(type: str, text: str):
    if type == 'debug':
        if DEBUG:
            print(colors.CYAN+ f'DEBUG | {text}')
    elif type == 'info':
        print(colors.GREEN+ f'INFO  | {text}')
    elif type == 'error':
        print(colors.RED+ f'ERROR | {text}')
    elif type == 'warn':
        print(colors.YELLOW+ f'WARN  | {text}')


def resourcePath(filaeName):
    if not DEBUG:
        return os.path.join(sys._MEIPASS, filaeName)
    return os.path.join(filaeName)


def PauseAndExit():
    input('\n    按下回车退出...')
    exit(0)


# main code.
def getJarFile(file_path: str):
    full_file_list = os.listdir(file_path)
    Log('debug', f'程序目录下完整文件列表: {full_file_list}')

    jar_file_list = []
    for item in full_file_list:
        Log('debug', f'正在校验: {item}')
        file_name, file_ext = os.path.splitext(item)
        if file_ext == '.jar':
            jar_file_list.append(item.replace(file_ext, ''))
            Log('info', f'检测到Jar文件: {file_name}'+'.jar')
    Log('debug', f'JAR文件队列: {jar_file_list}')
    return jar_file_list


def unzipjarFile(script_path: str, jar_file_name: str):
    unzip_flag = False

    timp_file_dir = os.path.join(script_path, 'temp')
    Log('info', f'提取jar文件至临时目录: [{timp_file_dir}].')

    if os.path.exists(timp_file_dir):
        Log('warn', f'存在临时文件夹，程序中止\n  请手动删除[{timp_file_dir}]目录后重新运行.')

    else:
        os.makedirs(timp_file_dir)
        try:
            jar_file = zipfile.ZipFile(os.path.join(script_path, jar_file_name+'.jar'), "r")
            for item in jar_file.namelist(): 
                Log('debug', f'提取JAR中文件: {item}')
                jar_file.extract(item, timp_file_dir)
            Log('info', f'成功.')
            unzip_flag = True

        except:
            Log('error', f'从JAR提取文件时发生错误.')
    return timp_file_dir, unzip_flag


def recoverFile(work_path: str):
    Log('info', f'开始汉化:')
    lang_file_list = os.listdir(resourcePath(os.path.join('lang')))
    work_dir_list = os.listdir(os.path.join(work_path, 'assets'))
    Log('info', f'已载入汉化文件包: {lang_file_list}')

    try:
        for dir_name in work_dir_list:
            if dir_name in lang_file_list:
                Log('info', f'需要文件包: {dir_name}')
                for lang_file in os.listdir(resourcePath(os.path.join('lang', dir_name, 'lang'))):
                    shutil.copy2( \
                    resourcePath(os.path.join('lang', dir_name, 'lang', lang_file)), \
                    os.path.join(work_path, 'assets', dir_name, 'lang', lang_file))
                    Log('info', f'成功向[{dir_name}]中添加语言文件[{lang_file}]')
    except:
        Log('error', f'对临时文件添加汉化文件时发生错误，瞅瞅硬盘满了没，或者用管理员权限运行试试.')
        return False
    Log('info', f'汉化完毕.')
    return True


def reJarFile(zip_path: str, work_path: str, file_name: str):
    Log('info', f'正在输出文件...')
    Log('debug', f'zip_path: {zip_path}, work_path: {work_path}')

    try:
        jarFile = zipfile.ZipFile(os.path.join(work_path, f'汉化-{file_name}_zh_CN.jar'), 'w', zipfile.ZIP_DEFLATED)

        for path, dir_list, file_list in os.walk(zip_path):  
            for file_name in file_list:  
                Log('debug', f'添加文件至压缩: {os.path.join(path, file_name)}')
                jarFile.write(os.path.join(path, file_name), os.path.join(path.replace(zip_path, ''), file_name))
        jarFile.close()
        Log('info', f'成功，已输出文件:[汉化-{file_name}_zh_CN.jar]')

    except PermissionError:
        Log('error', f'目录中存在已汉化文件[汉化-{file_name}_zh_CN.jar], 不要白嫖我做重复劳动捏')
        PauseAndExit()



if __name__ == '__main__':
    script_path = os.path.split(os.path.realpath(__file__))[0]

    jar_file_list, jar_count = getJarFile(script_path), 1
    Log('info', f'共检测到 {len(jar_file_list)} 个JAR文件.')

    for jar_file_name in jar_file_list:
        Log('info', f'开始处理第 {jar_count} 个JAR文件: [{jar_file_name}]')

        unzip_path, unzip_flag = unzipjarFile(script_path, jar_file_name)
        if not unzip_flag:
            PauseAndExit()
        else:
            if not recoverFile(unzip_path):
                PauseAndExit()
            else:
                reJarFile(unzip_path, script_path, jar_file_name)

        # Remove temp Dir.
        try:
            shutil.rmtree(path=unzip_path)
            Log('info', f'临时文件清理完毕.\n')
        except:
            Log('warn', f'清理临时文件遇到错误，请手动删除[{unzip_path}]目录')

        jar_count = jar_count +1

    Log('info', f'成功处理 {jar_count -1} 个文件.')
    Log('info', f'汉化度低于90%时欢迎到懒兵群内催更\n\n  感谢你使用懒兵汉化喵')
    PauseAndExit()