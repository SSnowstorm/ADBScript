import json
import os
import sys


def load_json_file(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data


def save_json_file(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def get_config_path():
    current_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    path = os.path.join(current_path, "config.json")
    return path


def load_conf():
    conf_path = get_config_path()
    data = load_json_file(conf_path)
    return data


if __name__ == "__main__":
    # conf_path = get_config_path()
    # print(conf_path)
    # data = load_json_file(conf_path)
    # print(data)
    # apk_type = data['apk_type']
    # print(apk_type)
    pass
