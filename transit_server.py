from fastapi import FastAPI, HTTPException
from utils import (long_perform,
                   app_ui_entry,
                   date_stamp,
                   installed_folder)
from utils import init_config

cfg = init_config()

app = FastAPI()


@app.post("/transit")
async def transit_endpoint(post_data: dict):
    # post_data 将包含从POST请求中接收到的参数
    # print("Received POST data:", post_data, type(post_data))
    argv = post_data.get("argv", "")
    long_perform(func_target=app_ui_entry,
                 name=date_stamp(),
                 args=(f"{cfg['python_executable']} {installed_folder()}/uikit/app_ui.py {argv}",))

    # 在这里你可以执行任何你想要的操作，比如处理参数，返回响应等
    # 启动命令uvicorn transit_server:app --reload --port 9090

    return {"message": "Data received successfully"}
