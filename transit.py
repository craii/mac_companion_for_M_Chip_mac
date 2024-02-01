import os
import sys
import json
import requests
from utils import init_config
cfg = init_config()


def transit() -> str:
    args = sys.argv
    print(f"transit参数接收成功：{args}")
    if len(args) != 2:
        return "(ONLY) 1 argv is needed for transit.py to jumpstart mac_companion UI for a conversation."

    try:
        # from config import cfg
        transit_port = cfg["transit_port"]
    except ImportError as e:
        print(f"transit_port import error, reason: {e} ")
        transit_port = 9090

    res = requests.post(url=f"http://127.0.0.1:{transit_port}/transit", data=json.dumps({"argv": args[1]}))

    # os.system('killall Terminal')

    return f"transit running complete:{res.text}"


if __name__ in "__main__":
    print(transit())
