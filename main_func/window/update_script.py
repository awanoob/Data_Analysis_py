
import os
import sys
import time

def replace_exe():
    current_exe = "D:\ProgramData\Anaconda3\python.exe"
    new_exe = "D:\ProgramData\Anaconda3\DataAnalysis_new.exe"
    backup_exe = current_exe + ".bak"

    # �ȴ�ԭ�����˳�
    time.sleep(1)

    # ���ݵ�ǰexe
    os.rename(current_exe, backup_exe)

    # �滻Ϊ��exe
    os.rename(new_exe, current_exe)

    # ɾ������
    os.remove(backup_exe)

    # �����°汾
    os.startfile(current_exe)

if __name__ == '__main__':
    replace_exe()
