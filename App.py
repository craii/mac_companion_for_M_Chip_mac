import os
import sys
import rumps

from utils import (installed_folder,
                   app_ui_entry,
                   guardian_server,
                   long_perform,
                   shutdown_process,
                   date_stamp,
                   free_port,
                   init_database,
                   init_config,
                   init_aiserver
                   )
from config import PROCESS


cfg = init_config()


class MenuBarApp(rumps.App):
    def __init__(self):
        super(MenuBarApp, self).__init__("")
        self.menu = ["Chat", "History", "database_folder"]
        self.icon = f"{installed_folder()}/images/icon.ico"  # 替换为你的应用图标路径
        self.title = ""

        init_database()

        # 启动ChatGLM 的 openai_like api
        long_perform(func_target=init_aiserver,
                     name="ChatGLM" + date_stamp(),
                     args=())

        # 启动copilot监听服务
        free_port(cfg['transit_port'])
        long_perform(func_target=guardian_server,
                     name=date_stamp(),
                     args=(f"cd {installed_folder()} && uvicorn transit_server:app --reload --port {cfg['transit_port']}",))

    @rumps.clicked("History")
    def open_menu_item(self, _):
        rumps.alert("Hello, Your App!")

    @rumps.clicked("Chat")
    def preferences_menu_item(self, _):
        long_perform(func_target=app_ui_entry,
                     name=date_stamp(),
                     args=(f"{cfg['python_executable']} {installed_folder()}/uikit/app_ui.py",))

    @rumps.clicked("Quit")
    def quit_menu_item(self, _):
        global PROCESS  # PROCESS is dict
        print(PROCESS)
        for p_name, p_process in PROCESS.items():
            shutdown_process(p_name)
        rumps.quit_application()


if __name__ == "__main__":
    app = MenuBarApp()
    app.run()
