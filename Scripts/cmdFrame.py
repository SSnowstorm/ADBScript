import os
import sys

import adbutils
from adbutils import adb
import inquirer


def keyword_combination(args: dict, packagename: dict):
    # 初始化返回字典
    # {'filter': ['glGetError exceeded.'], 'packagename': 'dev.sunray.xzkl', 'keyword': ['selfParty'],
    # 'devices': 'emulator-5554'}

    result = {}

    try:
        # 检查必要的键是否存在
        if 'project' not in args or 'keyword' not in args or 'devices' not in args:
            raise ValueError("Missing required keys in the input dictionary")

        # 提取项目名和关键字
        project, keyword = args['project'], args['keyword']

        # 获取包名并检查项目是否有效
        package = packagename.get(project)
        if package is None:
            raise ValueError("Invalid project name provided")

        result['packagename'] = package

        # 根据关键字决定逻辑
        if keyword == 'BattleInfo':
            result['keyword'] = ['this.m_EnemyInfo']
        elif keyword == 'AllInfo':
            result['keyword'] = None
        elif keyword == 'InstallLatest':
            result['keyword'] = 'InstallLatest'
        elif keyword == "SaveLog":
            result['keyword'] = None
        else:
            raise ValueError("Invalid keyword provided")

        # 处理设备信息
        result['devices'] = args['devices']
        # 记录用户选择的项目名
        result['project'] = args['project']
    except Exception as e:
        print('Invalid Input:\n', e)

    return result


def check_answer(project: list, keyword: list) -> dict:
    """
    创建带有选项的命令行，返回用户选择的选项对应的dict
    :return: 用户选择的选项与对应选项的name组合形成的dict
    """
    questions = [
        inquirer.List(name='project',
                      message="Select Project",
                      choices=project, ),
        inquirer.List(name='keyword',
                      message="Select Keyword",
                      choices=keyword,
                      ),
    ]

    d_list = get_device_list()
    # 有多个设备时增加一个单选框让用户选择具体设备的序列号
    if len(d_list) > 1:
        questions.append(inquirer.List(
            name='devices',
            message="Multiple devices are detected, please choose a single device",
            choices=d_list,
        ))
        answer = inquirer.prompt(questions)
    else:
        answer = inquirer.prompt(questions)
        answer.update({'devices': d_list[0]})
    return answer


def get_device_list() -> list:
    """
    获取模拟器列表并返回所有设备的序列号
    :return: 当前运行的所有模拟器的序列号list
    """
    device_list = []
    for d in adb.device_list():
        device_list.append(d.serial)
    return device_list


def create_frame(packagename, keyword, project, filtered_words):
    answer = check_answer(project=project, keyword=keyword)
    keywords = keyword_combination(answer, packagename)
    # filtered_words = ['glGetError exceeded.']
    args = {'filter': filtered_words}
    args.update(keywords)
    args.update({"choice": answer["keyword"]})
    args.update({"devices": answer["devices"]})
    return args


if __name__ == '__main__':
    # arguments = create_frame()
    # print('arguments:' + str(arguments))
    current_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    print(current_path)
    pass
