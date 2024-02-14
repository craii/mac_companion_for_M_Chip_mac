import os
import re
import subprocess
import multiprocessing
from typing import Callable
from datetime import datetime
from typing import Union

from config import PROCESS, cfg
from data_storage.sqlite_controller import *


def get_pid_using_port(port: str) -> Union[list, None]:
    # 构建 lsof 命令字符串
    command = f"lsof -i :{port}"
    # 使用 Popen 执行命令
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # 获取标准输出和标准错误输出
    output, error = process.communicate()
    # 打印输出结果（可选）
    # print("标准输出:\n", output)
    # print("标准错误输出:\n", error)
    # 解析输出以获取 PID
    lines = output.split('\n')
    pids = list()
    if len(lines) >= 2:
        for info in lines[1:]:
            process_info = info.split()

            if len(process_info) >= 2:
                pids.append(int(process_info[1]))

    return pids if pids else None


def free_port(port: str) -> bool:
    pids = get_pid_using_port(port)
    if pids is None:
        print(f"port： {port} is free")
        return True
    try:
        for pid in pids:
            os.system(f"kill -09 {pid}")
            print(f"the process({pid}) that occupied port({port}) has been killed")
        return True
    except Exception as e:
        print(f"Encounter an error when killing the process.(error:{e}) "
              f"\nYou may try to kill the process(es): {pids} manually.")
        return False


def installed_folder() -> str:
    return os.getcwd()


def date_string():
    _now = datetime.now()
    return f"{_now.date()}"


def date_stamp():
    _now = datetime.now()
    return f"_{_now.date()}_{_now.time()}"


def app_ui_entry(command: str) -> None:
    os.system(command)


def guardian_server(command: str) -> None:
    os.system(command)


def run_webui(command: str) -> None:
    os.system(command)


def long_perform(func_target: Callable, name: str, args: tuple) -> dict:
    _process = multiprocessing.Process(target=func_target, args=args, name=name)
    _process.daemon = True
    _process.start()
    global PROCESS
    PROCESS[name] = _process
    return PROCESS


def shutdown_process(p_name: str) -> str:
    running_process = PROCESS.get(p_name, None)
    print("closeing:", running_process)
    if None:
        return f"No running ui named {p_name}"

    if not isinstance(running_process, multiprocessing.Process):
        return ""

    running_process.terminate()

    return f"{p_name}: terminated. "


def init_database() -> None:
    db = SqliteController()
    db.init_db()
    db.close_connection("conversation")
    previous_settings = db.read_settings()
    if not previous_settings:
        insert_data_query = '''INSERT INTO settings (port, transit_port, system_prompt, aiserver_command, auto_prompt, auto_copy_last, python_executable)
                              VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(f'{cfg["port"]}', f'{cfg["transit_port"]}', f'{cfg["system_prompt"]}', f'{cfg["aiserver_command"]}', f'{cfg["auto_prompt"]}', f'{cfg["auto_copy_last"]}', f'{cfg["python_executable"]}')

        db.write(conn="settings", insert_data_query=insert_data_query)
    else:
        print(f"Previous settings existed...using it instead\n {previous_settings}")
    db.close_connection("settings")
    del db


def init_config() -> dict:
    try:
        db = SqliteController()
        db.init_db()
        db.close_connection("conversation")
        settings_in_db = db.read_settings()
        # print(settings_in_db)
        # print(cfg)
        return settings_in_db if settings_in_db is not None else cfg
    except Exception as e:
        print(e)
        return cfg


def init_aiserver(aiserver_command: str = None, port: str = "8001") -> None:
    free_port(port)
    command = init_config().get("aiserver_command", None) if aiserver_command is None else aiserver_command
    print(command)
    if command is None:
        return None
    os.system(command)


def message_concat(raw_msg: str) -> str:
    """
    :param raw_msg: response from chatglm model
    :return: concatenated html text for formatted presentation
    """
    pattern = re.compile(r"(```[^`]+```|.|.)")
    # 使用 finditer 函数找到所有匹配项
    matches = [match.group(0) for match in pattern.finditer(raw_msg)]
    refined_message = '''<p style="color: black">{}</p>'''
    trigger, tmp_msg = "```", str()
    tmp_result = list()
    for character in matches:
        if trigger not in character:
            tmp_msg += character
        else:
            tmp_result.append(refined_message.format(tmp_msg))
            tmp_result.append(f"<pre>{character}</pre>")
            tmp_msg = str()
            refined_message = '''<p style="color: black">{}</p>'''
    else:  # 处理全部都是常规文字，不含代码的回答
        tmp_result.append(refined_message.format(tmp_msg))

    print(tmp_result)
    return "".join(tmp_result)
