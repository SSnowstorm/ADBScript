import os
import subprocess


def install_latest_apk(adb_path, _apk_type, project_name, device, pkg_folder):
    apk_files = []

    _folder_path = pkg_folder[project_name]

    # 获取指定文件夹中所有的 APK 文件路径
    for root, dirs, files in os.walk(_folder_path):
        for file in files:
            if file.endswith(".apk") and _apk_type in file:
                apk_files.append(os.path.join(root, file))

    if not apk_files:
        print(f"No '{_apk_type}' APK file found in {_folder_path}")
        return

    # 找到最新的 APK 文件
    latest_apk = max(apk_files, key=os.path.getctime)

    # 使用 ADB 安装 APK 文件
    if not device:
        subprocess.run([adb_path, "install", "-r", latest_apk])
    else:
        subprocess.run([adb_path, "-s", device, "install", "-r", latest_apk])
    print(f"Latest '{_apk_type}' APK file '{latest_apk}' installed successfully")


if __name__ == "__main__":
    # 传入参数决定 APK 类型和文件夹地址（示例代码，仅供调试使用）
    apk_type = "debug"
    folder_path = "\\\\TOJOY-NAS\\fangcheng0505\\APK_MH5\\20240506"
    # folder_path = '\\\\TOJOY-NAS\\fangcheng0505\\APK_MH5'
    install_latest_apk(apk_type, folder_path)
