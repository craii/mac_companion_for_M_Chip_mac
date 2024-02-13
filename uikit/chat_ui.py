import json
import requests

from utils import (init_config,
                   message_concat)

from data_storage.sqlite_controller import SqliteController
from data_storage.message_storage import MessageStorage

from PySide6.QtCore import (Qt,
                            QObject,
                            Signal,
                            QRunnable,
                            QThreadPool,
                            Slot,
                            QTimer
)

from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QTextEdit,
)

cfg = init_config()


class WorkerSignals(QObject):

    errors = Signal(str)
    finish = Signal()
    result = Signal(str)


class PayloadWorker(QRunnable):

    def __init__(self, message: list):
        super().__init__()
        self.signals = WorkerSignals()
        self.messages = message

    def get_answer(self, message: list):
        answer = str()
        headers = {'Content-Type': 'application/json'}
        data = {"messages": message}
        result = requests.post(url=f'http://127.0.0.1:{cfg["port"]}/v1/chat/completions',
                               headers=headers,
                               data=json.dumps(data))
        answer += json.loads(result.text)["choices"][0]["message"]["content"]
        return answer

    @Slot()
    def run(self):
        result = str()
        try:
            result += self.get_answer(self.messages)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.errors.emit(str(e))
        else:
            self.signals.finish.emit()


class Chat(QWidget):

    def __init__(self, **kwargs):
        super().__init__()
        self.db = SqliteController()
        self.messenger = None
        self.history_frame_head = '''<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body><div style="max-width: 400px;margin: 20px auto;overflow: hidden;">'''
        self.history_frame_tail = '''</div></body></html>'''
        self.session_history = str()
        self.latest_response = str()
        self.messages = [{"role": "system", "content": cfg["system_prompt"]}]  # 用于模型的上下文推理能力
        self.init_text = kwargs.get("init_text", "")

        layout_V = QVBoxLayout()
        layout_H = QHBoxLayout()

        self.text_box = QTextEdit()
        self.input_box = QTextEdit()
        send_btn = QPushButton("发送")
        copy_btb = QPushButton("复制")

        layout_H.addWidget(self.input_box)
        layout_H.addWidget(send_btn)
        layout_H.addWidget(copy_btb)

        layout_V.addWidget(self.text_box)
        layout_V.addLayout(layout_H)

        self.text_box.setReadOnly(True)
        self.text_box.setLineWrapColumnOrWidth(20)
        if self.init_text:
            self.input_box.append(self.init_text)
            if cfg["auto_prompt"] == "YES":
                QTimer.singleShot(0, lambda: send_btn.click())
                pass
        self.input_box.setFocus()
        self.input_box.setFixedHeight(50)
        self.input_box.lineWrapMode()
        self.setLayout(layout_V)

        self.thread_pool = QThreadPool()

        send_btn.pressed.connect(self.messaging)
        copy_btb.pressed.connect(self.copy_last)

    def copy_last(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.latest_response)

    def messaging(self):
        prompts = self.input_box.toPlainText()
        self.input_box.clear()
        messages = {"role": "user", "content": f"{prompts}"}
        self.messages.append(messages)  # 补充模型上下文

        if self.messenger is None:
            self.messenger = MessageStorage(first_msg=prompts)
        self.messenger.write_message(msg=prompts, character="user")

        user_av = '''<img src="./images/user.png" alt="user" style="float: left;width: 26px;height: 26px; border-radius: 50%;margin-right: 10px;">'''
        question = f'''<div style="overflow: hidden;">{user_av}
                               <div style="float: left; max-width: 70%; background-color: #DCF8C6; padding: 30px; border-radius: 30px; margin-top: 5px;">
                               <p style="color: black">{prompts}</p></div></div>'''
        self.session_history += question
        all_history = self.history_frame_head + self.session_history + self.history_frame_tail
        self.text_box.setHtml(all_history)

        worker = PayloadWorker(self.messages)
        worker.signals.result.connect(self.results)
        worker.signals.errors.connect(self.errors)
        worker.signals.finish.connect(self.finish)
        self.thread_pool.start(worker)

    def results(self, s):
        raw_response = message_concat(s)
        messages = {"role": "assistant", "content": f"{s}"}
        self.messages.append(messages)

        print(self.messages)

        self.messenger.write_message(msg=s, character="robot")

        robot_av = '''<img src="./images/robot.png" alt="robot" style="float: left;width: 26px;height: 26px; border-radius: 50%;margin-right: 10px;">'''
        response = f'''<div style="overflow: hidden;">{robot_av}
                        <div style="float: left; max-width: 70%; background-color: #DCF8C6; padding: 30px; border-radius: 30px; margin-top: 5px;">
                        {raw_response}</div></div><br>'''

        self.session_history += response
        all_response = self.history_frame_head + self.session_history + self.history_frame_tail

        self.latest_response = s
        self.text_box.setHtml(all_response)
        self.input_box.clear()

        if cfg["auto_copy_last"] == "YES":
            self.copy_last()

        return s

    def errors(self, s):
        print(f"errors: {s}")
        return s

    def finish(self):
        print(f"finish")
