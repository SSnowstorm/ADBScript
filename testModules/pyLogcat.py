import os.path
import subprocess
import sys


# cmd = ["adb", '-s', 'emulator-5554', "logcat"]


def logcat(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except KeyboardInterrupt as e:
        raise e


def inFilter(_str: str, filter_list: list):
    if not filter_list:
        return False
    for item in filter_list:
        if item in _str:
            return True
    return False


def logOutput(log: str):
    sys.stdout.write('\n' + log)
    sys.stdout.flush()


def logWriteIn(file_path, log: str):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(log)
    except Exception as e:
        sys.stdout.write(f"写入文件发生异常：{e}")
        raise e


def createFile(filepath):
    dir = os.path.dirname(filepath)
    if not os.path.exists(filepath):
        with open(filepath,'w',encoding='utf-8') as file :
            file.write("")
            sys.stdout.write(f"文件已创建")


def printLog(adb_path, device, pkg_name, fileter: list, keyword: list):
    _command = [adb_path, '-s', device, "logcat", pkg_name]
    process = logcat(_command)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        l_log = line.decode('utf-8').strip()
        if inFilter(l_log, keyword) is True:
            logOutput(l_log)
            return
        if inFilter(l_log, fileter) is True:
            continue
        else:
            logOutput(l_log)


def saveLog(adb_path, device, filtered_word, filename, pkg_name):
    _command = [adb_path, '-s', device, "logcat", pkg_name]
    process = logcat(_command)
    print(f"filename:{filename}")
    while True:
        line = process.stdout.readline()
        if not line:
            break
        l_log = line.decode('utf-8').strip()
        if inFilter(l_log, filtered_word) is True:
            continue
        else:
            logWriteIn(filename, l_log)


if __name__ == '__main__':
    filter_word = ["glGetError exceeded."]
    keywords = ['selfParty']  # , 'Error occurs in an event listener'
    interst_word = ['jswrapper']
    # subprocess.run(["adb", '-s', 'emulator-5554', "logcat"])
    cmd = ["adb", '-s', 'emulator-5554', "logcat", "dev.sunray.xzkl"]
    printLog(cmd, fileter=filter_word, keyword=keywords)
    print(os.path.dirname(os.path.abspath(sys.argv[0])))
    pass
