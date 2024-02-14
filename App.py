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
                   init_aiserver,
                   run_webui
                   )
from config import PROCESS


cfg = init_config()


class MenuBarApp(rumps.App):
    def __init__(self):
        super(MenuBarApp, self).__init__("")
        self.menu = ["Chat", "History", "WebUI", "Total Quit"]
        self.icon = f"{installed_folder()}/images/icon.ico"  # 替换为你的应用图标路径
        self.title = ""

        init_database()

        # 启动ChatGLM 的 openai_like api
        long_perform(func_target=init_aiserver,
                     name=f"ChatGML_OpenAi_api_{date_stamp()}",
                     args=())

        # 启动copilot监听服务
        free_port(cfg['transit_port'])
        long_perform(func_target=guardian_server,
                     name=f"ListenCopilot_{date_stamp()}",
                     args=(f"cd {installed_folder()} && uvicorn transit_server:app --reload --port {cfg['transit_port']}",))

    @rumps.clicked("WebUI")
    def open_menu_item(self, _):
        installed_at = installed_folder()
        command = f"{installed_at}/chatglmcpp/bin/streamlit run {installed_at}/chatglm.cpp-chatglm3/examples/chatglm3_demo.py"
        try:
            long_perform(func_target=run_webui,
                         name=f"WebUI_{date_stamp()}",
                         args=(command,))
        except Exception as e:
            rumps.alert(f"failed on webui initiation, error: {e}")

    @rumps.clicked("Chat")
    def preferences_menu_item(self, _):
        long_perform(func_target=app_ui_entry,
                     name=f"ChatUI_{date_stamp()}",
                     args=(f"{cfg['python_executable']} {installed_folder()}/uikit/app_ui.py",))

    @rumps.clicked("Total Quit")
    def quit_menu_item(self, _):
        global PROCESS  # PROCESS is dict
        print(PROCESS)
        for p_name, p_process in PROCESS.items():
            shutdown_process(p_name)
        rumps.quit_application()


if __name__ == "__main__":
    app = MenuBarApp()
    app.run()
