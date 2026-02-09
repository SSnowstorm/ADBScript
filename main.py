import datetime
import os
import sys

from Scripts.timeOperate import count_down
from Scripts.cmdFrame import create_frame
from testModules.pyLogcat import printLog, saveLog
from testModules.pyInstallAPK import install_latest_apk
from testModules.pySaveLog import save_log
from Scripts.loadJson import load_conf

choice = ''


def get_adb_path():
    current_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    adb_path = os.path.join(current_path, 'adb', 'adb.exe')
    return adb_path


def main():
    # 加载配置并加工成函数需要的字典
    config = load_conf()
    proj_list = config["project"].keys()

    pkg_name, pkg_type, pkg_path = [], [], []

    if isinstance(config["project"], dict):
        for key, value in config["project"].items():
            pkg_name.append(value["packagename"])
            pkg_type.append(value["apk_type"])
            pkg_path.append(value["pkg_folder"])

    package_name = {k: v for k, v in zip(proj_list, pkg_name)}
    package_type = {k: v for k, v in zip(proj_list, pkg_type)}
    package_path = {k: v for k, v in zip(proj_list, pkg_path)}

    # 创建CMD窗口并提供设置的选项
    res = create_frame(packagename=package_name, keyword=config["keyword"], project=proj_list,
                       filtered_words=config["filtered_words"])

    # print(res)

    global choice
    choice = res['choice']

    _adb_path = get_adb_path()

    # 根据选择装包或者拉log决定逻辑
    if res['choice'] == 'InstallLatest':
        install_latest_apk(adb_path=_adb_path, _apk_type=package_type[res['project']], project_name=res['project'],
                           device=res['devices'], pkg_folder=package_path)
    elif res['choice'] == 'AllInfo' or res['choice'] == 'BattleInfo':
        printLog(adb_path=_adb_path, device=res['devices'], pkg_name=res['packagename'], fileter=res['filter'],
                 keyword=res['keyword'])
    elif res['choice'] == 'SaveLog':
        current_time = datetime.datetime.now().strftime("%m%d-%H%M")
        current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        file_name = str(res["devices"]) + f"_{current_time}.log"
        file_path = os.path.join(current_dir,file_name)
        save_log(adb_path=_adb_path, device=res["devices"], filtered_word=config["filtered_words"][0],
                 filename=str(res["devices"]) + f"_{current_time}.log", timeout=10)
        # saveLog(adb_path=_adb_path, device=res["devices"], filtered_word=config["filtered_words"][0],
        # filename=file_path, pkg_name=res['packagename'])


if __name__ == '__main__':
    try:
        main()
        count_down(seconds=10)
    except KeyboardInterrupt as e:
        print(e)
    finally:
        if choice == 'InstallLatest' or "SaveLog":
            count_down(seconds=10)
        else:
            count_down(minutes=1)
