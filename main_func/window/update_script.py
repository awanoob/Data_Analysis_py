
import os
import sys
import time

def replace_exe():
    current_exe = "D:\ProgramData\Anaconda3\python.exe"
    new_exe = "D:\ProgramData\Anaconda3\DataAnalysis_new.exe"
    backup_exe = current_exe + ".bak"

    # 等待原程序退出
    time.sleep(1)

    # 备份当前exe
    os.rename(current_exe, backup_exe)

    # 替换为新exe
    os.rename(new_exe, current_exe)

    # 删除备份
    os.remove(backup_exe)

    # 启动新版本
    os.startfile(current_exe)

if __name__ == '__main__':
    replace_exe()
