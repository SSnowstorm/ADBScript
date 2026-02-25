import datetime
import os
import sys

from Scripts.timeOperate import count_down
from Scripts.cmdFrame import create_frame
from testModules.pyLogcat import printLog, saveLog
from testModules.pyInstallAPK import install_latest_apk
from testModules.pySaveLog import save_log
from Scripts.loadJson import load_conf


def get_adb_path():
    current_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    adb_path = os.path.join(current_path, "adb", "adb.exe")
    return adb_path


def build_project_maps(config):
    """
    根据配置构建项目相关的映射：
    - project_names: 项目名列表
    - package_name:  项目 -> 包名
    - package_type:  项目 -> apk 类型
    - package_path:  项目 -> apk 所在目录
    """
    projects = config.get("project", {})
    if not isinstance(projects, dict):
        raise ValueError("`project` 字段在 config.json 中必须是一个字典")

    project_names = list(projects.keys())
    package_name = {k: v["packagename"] for k, v in projects.items()}
    package_type = {k: v["apk_type"] for k, v in projects.items()}
    package_path = {k: v["pkg_folder"] for k, v in projects.items()}

    return project_names, package_name, package_type, package_path


def handle_user_choice(selection, config, package_type, package_path, adb_path):
    """
    根据用户在交互界面中的选择执行对应逻辑。
    """
    choice = selection["choice"]

    if choice == "InstallLatest":
        install_latest_apk(
            adb_path=adb_path,
            _apk_type=package_type[selection["project"]],
            project_name=selection["project"],
            device=selection["devices"],
            pkg_folder=package_path,
        )
    elif choice in ("AllInfo", "BattleInfo"):
        printLog(
            adb_path=adb_path,
            device=selection["devices"],
            pkg_name=selection["packagename"],
            fileter=selection["filter"],
            keyword=selection["keyword"],
        )
    elif choice == "SaveLog":
        current_time = datetime.datetime.now().strftime("%m%d-%H%M")
        current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        file_name = f"{selection['devices']}_{current_time}.log"
        file_path = os.path.join(current_dir, file_name)

        save_log(
            adb_path=adb_path,
            device=selection["devices"],
            filtered_word=config["filtered_words"][0],
            filename=file_name,
            timeout=10,
        )
        # saveLog(adb_path=adb_path, device=selection["devices"], filtered_word=config["filtered_words"][0],
        #         filename=file_path, pkg_name=selection["packagename"])

    return choice


def main():
    # 加载配置并加工成函数需要的字典
    config = load_conf()

    project_names, package_name, package_type, package_path = build_project_maps(config)

    # 创建 CMD 窗口并提供设置的选项
    selection = create_frame(
        packagename=package_name,
        keyword=config["keyword"],
        project=project_names,
        filtered_words=config["filtered_words"],
    )

    adb_path = get_adb_path()

    # 根据选择装包或者拉 log 决定逻辑
    return handle_user_choice(selection, config, package_type, package_path, adb_path)


if __name__ == "__main__":
    choice = None  # 确保无论是否被中断，finally 中都能访问到 choice
    try:
        choice = main()
        count_down(seconds=10)
    except KeyboardInterrupt as e:
        print(e)
    finally:
        if choice in ("InstallLatest", "SaveLog"):
            count_down(seconds=10)
        else:
            count_down(minutes=1)
