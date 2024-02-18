import sys
from pathlib import Path
sys.path.append(f"{Path(__file__).resolve().parent.parent}")

from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QCheckBox,
    QPlainTextEdit
)

from utils import init_config
from data_storage.sqlite_controller import SqliteController


class Setting(QWidget):

    def __init__(self):
        super().__init__()
        self.cfg = init_config()
        layout_V = QVBoxLayout()  # v for vertical
        layout_H_sql = QHBoxLayout()  # H for horizontal
        layout_H_basic = QHBoxLayout()

        layout_H_py = QHBoxLayout()
        layout_H_ai = QHBoxLayout()

        layout_H_port = QHBoxLayout()
        layout_H_transit_port = QHBoxLayout()

        self.auto_copy_checkbox = QCheckBox("自动复制模型的最后一条回答")
        self.auto_run_checkbox = QCheckBox("服务进入时自动将选中文字作为prompt向模型提问")

        basic_prompt_title = QLabel("系统提示词")
        self.basic_prompt = QPlainTextEdit()

        aiserver_command_title = QLabel("AI服务器启动命令")
        self.aiserver_command = QPlainTextEdit()

        python_executable_title = QLabel("Python Excecutable")
        self.python_executable = QPlainTextEdit()

        ai_port_title = QLabel("模型端口")
        self.ai_port = QPlainTextEdit()

        transit_port_title = QLabel("监听端口")
        self.transit_port = QPlainTextEdit()

        # sql_title = QLabel("Sqlite路径")
        # sqlite_path = QPlainTextEdit()
        save_button = QPushButton("保存设置")
        save_button.pressed.connect(self.save_settings)

        # sqlite_path.setFixedHeight(32)
        self.basic_prompt.setFixedHeight(32)
        self.aiserver_command.setFixedHeight(32)
        self.python_executable.setFixedHeight(32)
        self.ai_port.setFixedHeight(32)
        self.transit_port.setFixedHeight(32)

        # layout_H_sql.addWidget(sql_title)
        # layout_H_sql.addWidget(sqlite_path)
        layout_H_basic.addWidget(basic_prompt_title)
        layout_H_basic.addWidget(self.basic_prompt)

        layout_V.addWidget(self.auto_copy_checkbox)
        layout_V.addWidget(self.auto_run_checkbox)

        layout_H_py.addWidget(python_executable_title)
        layout_H_py.addWidget(self.python_executable)

        layout_H_ai.addWidget(aiserver_command_title)
        layout_H_ai.addWidget(self.aiserver_command)

        layout_H_port.addWidget(ai_port_title)
        layout_H_port.addWidget(self.ai_port)

        layout_H_transit_port.addWidget(transit_port_title)
        layout_H_transit_port.addWidget(self.transit_port)

        layout_V.addLayout(layout_H_basic)
        layout_V.addLayout(layout_H_sql)
        layout_V.addLayout(layout_H_ai)
        layout_V.addLayout(layout_H_py)
        layout_V.addLayout(layout_H_port)
        layout_V.addLayout(layout_H_transit_port)

        layout_V.addWidget(save_button)
        self.setLayout(layout_V)

        self.basic_prompt.setPlainText(self.cfg["system_prompt"])
        if self.cfg["auto_copy_last"] == "YES":
            self.auto_copy_checkbox.setChecked(True)
        if self.cfg["auto_prompt"] == "YES":
            self.auto_run_checkbox.setChecked(True)
        if self.cfg["aiserver_command"]:
            self.aiserver_command.setPlainText(self.cfg["aiserver_command"])
        if self.cfg["python_executable"]:
            self.python_executable.setPlainText(self.cfg["python_executable"])
        if self.cfg["port"]:
            self.ai_port.setPlainText(self.cfg["port"])
        if self.cfg["transit_port"]:
            self.transit_port.setPlainText(self.cfg["transit_port"])


    def save_settings(self):
        port = self.ai_port.toPlainText()
        transit_port = self.transit_port.toPlainText()
        system_prompt = self.basic_prompt.toPlainText()
        aiserver_command = self.aiserver_command.toPlainText()
        auto_prompt = "YES" if self.auto_run_checkbox.isChecked() else "NO"
        auto_copy_last = "YES" if self.auto_copy_checkbox.isChecked() else "NO"
        python_executable = self.python_executable.toPlainText()
        db = SqliteController()
        db.connect_db("settings")
        db.update_settings(port=port,
                           transit_port=transit_port,
                           system_prompt=system_prompt,
                           aiserver_command=aiserver_command,
                           auto_prompt=auto_prompt,
                           auto_copy_last=auto_copy_last,
                           python_executable=python_executable,
                           )







