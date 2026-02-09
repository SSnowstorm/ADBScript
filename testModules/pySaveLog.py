import subprocess
import threading
import time
import os
import signal
from Scripts.timeOperate import count_down
import shlex


def run_command(cmd, timeout):
    # 开始子进程
    process = subprocess.Popen(cmd, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                               universal_newlines=True, bufsize=0, encoding="UTF-8")

    # 中止子进程
    # def terminate_process():
    #     try:
    #         process.send_signal(signal.CTRL_BREAK_EVENT)
    #         print("Process terminated")
    #     except Exception as e:
    #         print(f"Error terminating process: {e}")
    #         return e
    #
    # timer = threading.Timer(timeout, terminate_process)
    # timer.start()
    #
    # # 增加显示用的倒计时
    # count_down(seconds=timeout - 1)
    #
    # stdout, stderr = process.communicate()
    #
    # # 倒计时结束前完成任务则取消倒计时
    # timer.cancel()
    try:
        stdout, stderr = process.communicate()
        return stdout, stderr
    except Exception as e:
        raise e


def save_log(adb_path, device, filtered_word, filename, timeout):
    if timeout is None:
        timeout = 10
    print(f"filtered_word:{filtered_word}")
    filtered_word = "\'" + filtered_word + "\'"
    # print(f"filtered_word processed:{filtered_word}")
    # command = f"adb_path adb -s {device} shell \"logcat | grep -v {filtered_word}\" > {filename}"
    command = [adb_path, '-s', device, "shell", f"logcat | grep -v {filtered_word}", ">", filename]
    # command = [adb_path, '-s', device, "logcat", ">", filename]
    # print(shlex.join(command))
    # [adb_path, '-s', device, "logcat", pkg_name]
    try:
        while True:
            run_command(command, timeout)
    except Exception as e:
        print(e)
        raise e


if __name__ == '__main__':
    command = "adb -s emulator-5554 shell \"logcat | grep -v 'glGetError'\" > logcatByCode.txt"
    sp_command = shlex.split(command)
    print(sp_command)
    command2 = "adb -s emulator-5554 logcat -g"
    run_command(command2, 5)
    pass
