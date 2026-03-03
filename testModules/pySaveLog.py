import shlex
import subprocess
import time


def run_command(cmd, timeout):
    # 开始子进程
    process = subprocess.Popen(
        cmd,
        shell=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        universal_newlines=True,
        bufsize=0,
        encoding="UTF-8",
    )

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
    # 逐行读取 adb logcat 并写入文件，支持超时或 Ctrl+C 退出。
    start_ts = time.monotonic()
    line_count = 0
    process = None

    try:
        with open(filename, "w", encoding="utf-8") as out_f:
            process = subprocess.Popen(
                [adb_path, "-s", device, "logcat"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )

            while True:
                if timeout is not None and (time.monotonic() - start_ts) >= timeout:
                    break

                line = process.stdout.readline() if process.stdout is not None else ""
                if not line:
                    break

                if filtered_word and filtered_word in line:
                    continue

                out_f.write(line)
                line_count += 1

    except KeyboardInterrupt as e:
        raise e
    except Exception as e:
        print(e)
        raise e
    finally:
        if process is not None:
            try:
                process.terminate()
            except Exception:
                pass
            try:
                process.wait(timeout=2)
            except Exception:
                pass

            print(f"save_log done, wrote {line_count} lines to {filename}")


if __name__ == "__main__":
    command = "adb -s emulator-5554 shell \"logcat | grep -v 'glGetError'\" > logcatByCode.txt"
    sp_command = shlex.split(command)
    print(sp_command)
    command2 = "adb -s emulator-5554 logcat -g"
    run_command(command2, 5)
    pass
